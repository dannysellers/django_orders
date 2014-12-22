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


class Inventory(models.Model):
	owner = models.ForeignKey(Customer)
	itemid = models.IntegerField(unique = True)
	quantity = models.IntegerField(default = 1)
	length = models.FloatField(default = 1.00, max_length = 5)
	width = models.FloatField(default = 1.00, max_length = 5)
	height = models.FloatField(default = 1.00, max_length = 5)
	volume = models.FloatField(default = 1.00, max_length = 5)
	palletized = models.BooleanField(default = False)
	arrival = models.DateField()
	departure = models.DateField()
	status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)
	storage_fees = models.FloatField(default = 0.05)

	def __unicode__ (self):
		return 'Item {}'.format(self.itemid)

	class Meta:
		verbose_name_plural = 'inventory'


class BaseOperation(models.Model):
	item = models.ForeignKey(Inventory)
	user = models.ForeignKey(User)

	class Meta:
		abstract = True


class Operation(models.Model):
	# TODO: Add way to distinguish types of operations
	# TODO: Make sure operations are sequential & non-overlapping
	# Foreign keys weren't behaving properly when these inherited from BaseOperation.
	# Will change this back later
	item = models.ForeignKey(Inventory)
	user = models.ForeignKey(User)
	dt = models.DateTimeField()
	op_code = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.item.itemid, self.op_code)


class Shipment(models.Model):
	"""	Each Inventory object has multiple Operations and one Shipment. Shipments extend
	the Operation base class and include billing information (labor time,
	additional costs, et cetera). """

	item = models.ForeignKey(Inventory)
	user = models.ForeignKey(User)
	start = models.DateTimeField()
	finish = models.DateTimeField()
	labor_time = models.IntegerField()

	def __unicode__(self):
		return 'Shipment {}, Item {}'.format(self.id, self.item.itemid)


class OptExtras(models.Model):
	shipment = models.ForeignKey(Shipment)
	quantity = models.IntegerField(default = 1)
	unit_cost = models.FloatField()
	description = models.TextField()
	# Enable choice of preselected options, or creation of new type

	def __unicode__(self):
		return '{}x {}: ${}'.format(self.quantity, self.description, self.unit_cost)