# import os
from django.test import TestCase
from django.test.client import Client
from models import *
from datetime import date, datetime


############
# DATABASE #
############

class CustomerFactoryTest(TestCase):
	def setUp(self):
		self.customer = Customer.objects.create_customer(name = "Test Customer",
														 email = "test@domain.com",
														 acct = 11111)

	def test_customer_attrs(self):
		self.assertEqual(self.customer.name, "Test Customer")
		self.assertEqual(self.customer.email, "test@domain.com")
		self.assertEqual(self.customer.acct, 11111)
		self.assertEqual(self.customer.createdate, date.today())
		self.assertEqual(self.customer.notes, "notes")
		self.assertEqual(self.customer.status, 1)


class ItemShipmentFactoryTest(TestCase):
	def setUp(self):
		self.customer = Customer.objects.create_customer(name = "Test Customer",
														 email = "test@domain.com",
														 acct = 11111)
		self.shipment = Shipment.objects.create_shipment(owner = self.customer,
														 palletized = True,
														 labor_time = 60,
														 notes = "notes",
														 tracking_number = 1234567890)
		self.item = Inventory.objects.create_inventory(shipset = self.shipment,
													   length = 5.0,
													   width = 5.0,
													   height = 5.0)

	def test_shipment_attrs(self):
		self.assertEqual(self.shipment.shipid, Shipment.objects.count())
		self.assertEqual(self.shipment.arrival, date.today())
		self.assertEqual(self.shipment.status, 0)
		self.assertEqual(self.shipment.owner, self.customer)
		self.assertEqual(self.shipment.palletized, True)
		self.assertEqual(self.shipment.labor_time, 60)
		self.assertEqual(self.shipment.status, 0)
		self.assertEqual(self.shipment.notes, "notes")
		self.assertEqual(self.shipment.tracking_number, 1234567890)

	def test_item_attrs(self):
		self.assertEqual(self.item.itemid, Inventory.objects.count())
		self.assertEqual(self.item.owner, self.customer)
		self.assertEqual(self.item.arrival, date.today())

		_length = self.item.length
		_width = self.item.width
		_height = self.item.height
		_volume = float(_length) * float(_width) * float(_height)
		self.assertEqual(self.item.volume, _volume)
		self.assertEqual(self.item.storage_fees, _volume * UNIT_STORAGE_FEE)
		self.assertEqual(self.item.status, 0)

	def test_shipment_ops(self):
		ship_ops = list(self.shipment.shipoperation_set.all())
		self.assertEqual(self.shipment.status, len(ship_ops) - 1)
		self.assertEqual(self.shipment.get_status_display(), int(ship_ops[-1].op_code))

	def test_item_ops(self):
		item_ops = list(self.item.itemoperation_set.all())
		self.assertEqual(self.item.status, len(item_ops) - 1)
		self.assertEqual(self.item.get_status_display(), int(item_ops[-1].op_code))


# class ItemOpTestCases(TestCase):
# 	def setUp (self):
# 		self.itemlist = Inventory.objects.all()
#
# 	def test_item_op_equality (self):
# 		"""
# 		Tests that each Inventory object has the correct number
# 		of ItemOperation objects associated with it.
# 		"""
# 		for item in self.itemlist:
# 			iocount = ItemOperation.objects.filter(item = item).count() + 1
# 			self.assertEqual(item.status, iocount)


# class ShipOpTestCases(TestCase):
# 	def setUp (self):
# 		self.shipmentlist = Shipment.objects.all()
#
# 	def test_shipment_op_equality (self):
# 		"""
# 		Confirms that each shipment has the correct number
# 		of associated ShipOperation objects.
# 		"""
# 		for shipment in self.shipmentlist:
# 			socount = Shipment.objects.filter(shipment = shipment).count() + 1
# 			self.assertEqual(shipment.status, socount)


#########
# VIEWS #
#########


# class InventoryViewTestCases(TestCase):
# 	def setUp (self):
# 		inv_status_codes = [i[0] for i in INVENTORY_STATUS_CODES]
# 		inv_status_displays = [i[1] for i in INVENTORY_STATUS_CODES]
#
# 	def test_all_items (self):
# 		c = Client()
# 		response = c.get('/inventory')


###########
# WEBSITE #
###########


# class LogInTestCase(TestCase):
# def setUp(self):
# 		self.login_info = {'username': 'asdf', 'password': 'password'}
#
# 	def test_login (self):
# 		c = Client()
# 		response = c.post('/login/', self.login_info)
# 		self.assertEqual(response.status_code, 200)
