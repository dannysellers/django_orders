from django.db import models
from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.db.models.signals import post_save

import managers


UNIT_STORAGE_FEE = 0.05

CUSTOMER_STATUS_CODES = (
	('0', 'Inactive'),
	('1', 'Active'),
)

INVENTORY_STATUS_CODES = (
	('0', 'Inducted'),
	('1', 'Order received'),
	('2', 'Order started'),
	('3', 'Order completed'),
	('4', 'Shipped'),
)


class Customer(models.Model):
	name = models.CharField(max_length = 128, unique = False)
	acct = models.IntegerField(max_length = 5, primary_key = True, unique = True)
	email = models.EmailField()
	status = models.CharField(max_length = 1, choices = CUSTOMER_STATUS_CODES)
	createdate = models.DateField()
	closedate = models.DateField(null = True)
	notes = models.TextField()

	objects = managers.CustomerManager()

	def __unicode__ (self):
		return '{}: {}'.format(self.acct, self.name)


class Shipment(models.Model):
	owner = models.ForeignKey(Customer)
	shipid = models.IntegerField(unique = True)
	palletized = models.BooleanField(default = False)
	arrival = models.DateField()
	departure = models.DateField(null = True)
	labor_time = models.IntegerField()
	notes = models.TextField(null = True)
	tracking_number = models.CharField(max_length = 30, null = True)
	status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	objects = managers.ShipmentManager()

	def __unicode__ (self):
		return 'Acct #{}, Shipment {}'.format(self.owner.acct, self.shipid)

	def save (self, *args, **kwargs):
		if 'user' in args[0]:
			ShipOperation.objects.create_operation(shipment = self,
												   user = args[0]['user'],
												   op_code = self.status)
			super(Shipment, self).save()
		else:
			# raise something
			print("No user passed for Shipment status update request!: Shipment {}".format(self.shipid))
			pass


class Inventory(models.Model):
	shipset = models.ForeignKey(Shipment)
	owner = models.ForeignKey(Customer)
	itemid = models.IntegerField(unique = True, primary_key = True)
	length = models.FloatField(default = 1.00, max_length = 5)
	width = models.FloatField(default = 1.00, max_length = 5)
	height = models.FloatField(default = 1.00, max_length = 5)
	volume = models.FloatField(default = 1.00, max_length = 5)
	storage_fees = models.FloatField(default = UNIT_STORAGE_FEE)
	status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)
	arrival = models.DateField()
	departure = models.DateField(null = True)

	objects = managers.InventoryManager()

	def __unicode__ (self):
		return 'Item {}'.format(self.itemid)

	def save(self, *args, **kwargs):
		if 'user' in args[0]:
			ItemOperation.objects.create_operation(item = self,
												   user = args[0]['user'],
												   op_code = self.status)
			super(Inventory, self).save()
		else:
			# raise ???
			print("No user passed for Inventory status update request!: Item {}".format(self.itemid))
			pass

	class Meta:
		verbose_name_plural = 'inventory'


class Operation(models.Model):
	user = models.ForeignKey(User)
	dt = models.DateTimeField()
	op_code = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	class Meta:
		abstract = True


class ShipOperation(Operation):
	shipment = models.ForeignKey(Shipment)

	objects = managers.ShipOpManager()

	class Meta:
		verbose_name = "shipment operation"

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.shipment.shipid, self.op_code)


class ItemOperation(Operation):
	item = models.ForeignKey(Inventory)

	objects = managers.ItemOpManager()

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.item.itemid, self.op_code)


class OptExtras(models.Model):
	shipment = models.ForeignKey(Shipment)
	quantity = models.IntegerField(default = 1)
	unit_cost = models.FloatField()
	total_cost = models.FloatField()
	description = models.TextField()

	objects = managers.OptExtraManager()

	def __unicode__ (self):
		return '{} x {}: ${}'.format(self.quantity, self.description, self.unit_cost)