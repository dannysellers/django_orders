from django.db import models


CUSTOMER_STATUS_CODES = (
	('0', 'inactive'),
	('1', 'active'),
)

INVENTORY_STATUS_CODES = (
	('0', 'inventory_received'),
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
	closedate = models.DateField(null=True, blank=True)  # blank makes optional at init

	def __unicode__(self):
		return '{}: {}'.format(self.acct, self.name)


class Inventory(models.Model):
	owner = models.ForeignKey(Customer)
	itemid = models.IntegerField(unique=True)
	quantity = models.IntegerField(default=1)
	weight = models.IntegerField(default=1)
	palletized = models.BooleanField(default=False)
	palletweight = models.IntegerField(default=0)
	arrival = models.DateField()
	departure = models.DateField()
	status = models.CharField(max_length=1, choices=INVENTORY_STATUS_CODES)
	storage_fees = models.IntegerField()

	def __unicode__(self):
		return '<Item {}>'.format(self.itemid)


class Operation(models.Model):
	item = models.ForeignKey(Inventory)
	start = models.DateTimeField()
	finish = models.DateTimeField()

	def __unicode__(self):
		return '<Op started {}>'.format(self.start)