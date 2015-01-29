from django.db import models
from django.db.models import Manager
# from django.utils import timezone
from datetime import date, datetime

from audit_log.models import AuthStampedModel
from audit_log.models.managers import AuditLog
# from audit_log.models.fields import CreatingUserField

# import managers


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


class CustomerManager(Manager):
	def create_customer (self, name, email, acct):
		_customer = self.create(name = name, email = email,
								createdate = date.today(), status = 1,
								notes = "notes", acct = int(acct))
		print("Created {0}: {1}".format(_customer.name, _customer.acct))
		return _customer


class Customer(models.Model):
	name = models.CharField(max_length = 128, unique = False)
	acct = models.IntegerField(max_length = 5, primary_key = True, unique = True)
	# TODO: Add hidden account ID so that the front-facing one can be changed?
	email = models.EmailField()
	status = models.CharField(max_length = 1, choices = CUSTOMER_STATUS_CODES)
	createdate = models.DateField()
	closedate = models.DateField(null = True)
	notes = models.TextField()

	objects = CustomerManager()

	def __unicode__ (self):
		return '{}: {}'.format(self.acct, self.name)


class ShipmentManager(Manager):
	def create_shipment (self, owner, palletized, labor_time, notes, tracking_number):
		shipid = Shipment.objects.count() + 1
		arrival = date.today()
		_shipment = self.create(owner = owner, shipid = shipid, palletized = palletized,
								arrival = arrival, labor_time = labor_time, notes = notes,
								tracking_number = tracking_number)
		print("Created Ship ID: {}".format(_shipment.shipid))
		return _shipment


class Shipment(AuthStampedModel):
	owner = models.ForeignKey(Customer)
	shipid = models.IntegerField(unique = True)
	palletized = models.BooleanField(default = False)
	arrival = models.DateField()
	departure = models.DateField(null = True)
	labor_time = models.IntegerField()
	notes = models.TextField(null = True)
	tracking_number = models.CharField(max_length = 30, null = True)
	status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	objects = ShipmentManager()
	audit_log = AuditLog()

	def __unicode__ (self):
		return 'Acct #{}, Shipment {}'.format(self.owner.acct, self.shipid)

	def save (self, *args, **kwargs):
		super(Shipment, self).save()
		ShipOperation.objects.create_operation(shipment = self,
											   op_code = self.status)


class InventoryManager(Manager):
	def create_inventory (self, shipset, length, width, height):
		itemid = Inventory.objects.count() + 1
		owner = shipset.owner
		arrival = shipset.arrival
		volume = float(length) * float(width) * float(height)
		storage_fees = volume * UNIT_STORAGE_FEE
		status = 0
		_item = self.create(itemid = itemid, shipset = shipset, length = length,
							width = width, height = height,
							owner = owner, arrival = arrival,
							volume = volume, storage_fees = storage_fees,
							status = status)
		print("Created Item ID: {}".format(_item.itemid))
		return _item


class Inventory(AuthStampedModel):
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
	audit_log = AuditLog()

	def __unicode__ (self):
		return 'Item {}'.format(self.itemid)

	def save(self, *args, **kwargs):
		super(Inventory, self).save()
		ItemOperation.objects.create_operation(item = self,
											   op_code = self.status)

	class Meta:
		verbose_name_plural = 'inventory'


class Operation(AuthStampedModel):
	"""
	Base class for ShipOperation and ItemOperation, the
	only difference between which is the ForeignKey relation
	"""
	# user = CreatingUserField(related_name = 'created_ops')
	dt = models.DateTimeField()
	op_code = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

	class Meta:
		abstract = True


class ShipOpManager(Manager):
	def create_operation (self, shipment, op_code):
		_op = self.create(shipment = shipment, dt = datetime.now(), op_code = op_code)
		# TODO: Why are Ops getting created the number of times there are items in the carton set?
		print("Created Op {0} on Shipment {1}".format(_op.op_code, _op.shipment))
		return _op


class ShipOperation(Operation):
	shipment = models.ForeignKey(Shipment)

	objects = ShipOpManager()

	class Meta:
		verbose_name = "shipment operation"

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.shipment.shipid, self.op_code)


class ItemOpManager(Manager):
	def create_operation (self, item, op_code):
		_op = self.create(item = item, dt = datetime.now(), op_code = op_code)
		print("Created Op {0} on Item {1}".format(_op.op_code, _op.item))
		return _op


class ItemOperation(Operation):
	item = models.ForeignKey(Inventory)

	objects = ItemOpManager()

	def __unicode__ (self):
		return 'Item {}, Code {}'.format(self.item.itemid, self.op_code)


class OptExtraManager(Manager):
	def create_optextra (self, shipment, quantity, unit_cost, description):
		_total = unit_cost * quantity
		_extra = self.create(shipment = shipment, quantity = quantity,
							 unit_cost = unit_cost, total_cost = _total,
							 description = description)
		print("Created {} extra {} on Ship {}".format(_extra.quantity, _extra.description, _extra.shipment))
		return _extra


class OptExtras(models.Model):
	shipment = models.ForeignKey(Shipment)
	quantity = models.IntegerField(default = 1)
	unit_cost = models.FloatField()
	total_cost = models.FloatField()
	description = models.TextField()

	objects = OptExtraManager()

	def __unicode__ (self):
		return '{} x {}: ${}'.format(self.quantity, self.description, self.unit_cost)