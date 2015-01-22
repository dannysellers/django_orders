from models import *

from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User


class CustomerManager(models.Manager):
	def create_customer (self, name, email, acct):
		_customer = self.create(name = name, email = email,
								createdate = date.today(), status = 1,
								notes = "notes", acct = acct)
		print("Created {0}: {1}".format(_customer.name, _customer.acct))


class ShipmentManager(models.Manager):
	def create_shipment (self, owner, palletized, labor_time, notes, tracking_number):
		shipid = len(Shipment.objects.all()) + 1
		arrival = date.today()
		_shipment = self.create(owner = owner, shipid = shipid, palletized = palletized,
								arrival = arrival, labor_time = labor_time, notes = notes,
								tracking_number = tracking_number)
		print("Created Ship ID: {}".format(_shipment.shipid))


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


class ItemOpManager(models.Manager):
	def create_operation (self, item, user, op_code):
		_op = self.create(item = item, user = user,
						  dt = datetime.now(), op_code = op_code)
		print("Created Op {0} on Item {1}".format(_op.op_code, _op.item))


class ShipOpManager(models.Manager):
	def create_operation (self, shipment, user, op_code):
		_op = self.create(shipment = shipment, user = user,
						  dt = datetime.now(), op_code = op_code)
		print("Created Op {0} on Shipment {1}".format(_op.op_code, _op.shipment))


class OptExtraManager(models.Manager):
	def create_optextra (self, shipment, quantity, unit_cost, description):
		_total = unit_cost * quantity
		_extra = self.create(shipment = shipment, quantity = quantity,
							 unit_cost = unit_cost, total_cost = _total,
							 description = description)
		print("Created {} extra {} on Ship {}".format(_extra.quantity, _extra.description, _extra.shipment))