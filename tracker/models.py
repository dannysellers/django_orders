from django.db import models


CUSTOMER_STATUS_CODES = (
	('0', 'inactive'),
	('1', 'active'),
)

INVENTORY_STATUS_CODES = (
	('0', 'inducted'),
	('1', 'order_received'),
	('2', 'order_begun'),
	('3', 'order_completed'),
	('4', 'shipped'),
)


class Customer(models.Model):
	name = models.CharField(max_length=128, unique=False)
	acct = models.IntegerField(max_length=5, primary_key=True, unique=True)
	email = models.EmailField()
	status = models.CharField(max_length=1, choices=CUSTOMER_STATUS_CODES)
	createdate = models.DateField()
	closedate = models.DateField()

	def __unicode__(self):
		return '{}: {}'.format(self.acct, self.name)


class Inventory(models.Model):
	owner = models.ForeignKey(Customer)
	itemid = models.IntegerField(unique=True)
	quantity = models.IntegerField(default=1)
	length = models.FloatField(default=1.00, max_length=5)
	width = models.FloatField(default=1.00, max_length=5)
	height = models.FloatField(default=1.00, max_length=5)
	volume = models.FloatField(default=1.00, max_length=5)
	palletized = models.BooleanField(default=False)
	# palletweight = models.IntegerField(default=0)
	# This may not be the best implementation (necessary?),
	# cause each item does not have its own pallet / tracking
	# pallets is silly
	arrival = models.DateField()
	departure = models.DateField()
	status = models.CharField(max_length=1, choices=INVENTORY_STATUS_CODES, default=0)
	storage_fees = models.FloatField(default=0.05)

	# Handle operations as properties of items? Or vice-versa

	# def __init__(self):
	# 	self.storage_fees = self.weight * self.quantity

	def __unicode__(self):
		return 'Item {}'.format(self.itemid)


class Operation(models.Model):
	# TODO: Add way to distinguish types of operations
	# TODO: Settle list of types of ops
	item = models.ForeignKey(Inventory)
	start = models.DateTimeField()
	finish = models.DateTimeField()

	def __unicode__(self):
		return 'Op started {}'.format(self.start)