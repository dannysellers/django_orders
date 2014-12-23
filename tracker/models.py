from django.db import models
from django.contrib.auth.models import User


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
	closedate = models.DateField()
	notes = models.TextField()

	def __unicode__ (self):
		return '{}: {}'.format(self.acct, self.name)


class Shipment(models.Model):
	owner = models.ForeignKey(Customer)
	shipid = models.IntegerField(unique = True)
	palletized = models.BooleanField(default = False)
	arrival = models.DateTimeField()
	departure = models.DateTimeField()
	labor_time = models.IntegerField()
	notes = models.TextField()
	tracking_number = models.CharField(max_length = 30)

	def __unicode__(self):
		return 'Acct #{}, Shipment {}'.format(self.owner.acct, self.shipid)


class Inventory(models.Model):
	shipset = models.ForeignKey(Shipment)
	itemid = models.IntegerField(unique = True)
	length = models.FloatField(default = 1.00, max_length = 5)
	width = models.FloatField(default = 1.00, max_length = 5)
	height = models.FloatField(default = 1.00, max_length = 5)
	volume = models.FloatField(default = 1.00, max_length = 5)
	storage_fees = models.FloatField(default = 0.05)
	status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	# def __init__(self):
	# 	self.owner = self.shipset.owner
	# 	super(Inventory, self).__init__()

	def __unicode__(self):
		return 'Item {}'.format(self.itemid)

	class Meta:
		verbose_name_plural = 'inventory'


class Operation(models.Model):
	item = models.ForeignKey(Inventory)
	user = models.ForeignKey(User)
	dt = models.DateTimeField()
	op_code = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)
	notes = models.TextField()  # necessary?

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.item.itemid, self.op_code)


class OptExtras(models.Model):
	shipment = models.ForeignKey(Shipment)
	quantity = models.IntegerField(default = 1)
	unit_cost = models.FloatField()
	description = models.TextField()

	def __unicode__(self):
		return '{}x {}: ${}'.format(self.quantity, self.description, self.unit_cost)