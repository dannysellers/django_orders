from datetime import date, datetime

from django.db import models
from django.contrib.auth.models import User


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


class CustomerManager(models.Manager):
	def create_customer (self, name, email, acct):
		_customer = self.create(name = name, email = email,
								createdate = date.today(), status = 1,
								notes = "notes", acct = acct)
		print("Created {0}: {1}".format(_customer.name, _customer.acct))


class Customer(models.Model):
	name = models.CharField(max_length = 128, unique = False)
	acct = models.IntegerField(max_length = 5, primary_key = True, unique = True)
	email = models.EmailField()
	status = models.CharField(max_length = 1, choices = CUSTOMER_STATUS_CODES)
	createdate = models.DateField()
	closedate = models.DateField(null = True)
	notes = models.TextField()

	objects = CustomerManager()

	def __unicode__ (self):
		return '{}: {}'.format(self.acct, self.name)


class ShipmentManager(models.Manager):
	def create_shipment (self, owner, palletized, labor_time, notes, tracking_number):
		shipid = len(Shipment.objects.all()) + 1
		arrival = date.today()
		_shipment = self.create(owner = owner, shipid = shipid, palletized = palletized,
					arrival = arrival, labor_time = labor_time, notes = notes,
					tracking_number = tracking_number)
		print("Created Ship ID: {}".format(_shipment.shipid))


class Shipment(models.Model):
	owner = models.ForeignKey(Customer)
	shipid = models.IntegerField(unique = True)
	palletized = models.BooleanField(default = False)
	arrival = models.DateField()
	departure = models.DateField(null = True)
	labor_time = models.IntegerField()
	notes = models.TextField(null = True)
	tracking_number = models.CharField(max_length = 30, null = True)

	objects = ShipmentManager()

	def __unicode__ (self):
		return 'Acct #{}, Shipment {}'.format(self.owner.acct, self.shipid)


class InventoryManager(models.Manager):
	def create_inventory (self, shipset, length, width, height):
		itemid = len(Inventory.objects.all()) + 1
		owner = shipset.owner
		arrival = shipset.arrival
		volume = length * width * height
		storage_fees = volume * UNIT_STORAGE_FEE
		status = 0
		_item = self.create(itemid = itemid, shipset = shipset, length = length,
					width = width, height = height,
					owner = owner, arrival = arrival,
					volume = volume, storage_fees = storage_fees,
					status = status)
		print("Created Item ID: {}".format(_item.itemid))


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

	objects = InventoryManager()

	def __unicode__ (self):
		return 'Item {}'.format(self.itemid)

	class Meta:
		verbose_name_plural = 'inventory'


class OperationManager(models.Manager):
	def create_operation (self, item, user, op_code):
		_op = self.create(item = item, user = user,
					dt = datetime.now(), op_code = op_code)
		print("Created Op {0}: {1}".format(_op.op_code, _op.item))


class Operation(models.Model):
	item = models.ForeignKey(Inventory)
	user = models.ForeignKey(User)
	dt = models.DateTimeField()
	op_code = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	objects = OperationManager()

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.item.itemid, self.op_code)


class OptExtras(models.Model):
	shipment = models.ForeignKey(Shipment)
	quantity = models.IntegerField(default = 1)
	unit_cost = models.FloatField()
	description = models.TextField()

	def __unicode__ (self):
		return '{}x {}: ${}'.format(self.quantity, self.description, self.unit_cost)