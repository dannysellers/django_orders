from django.test import TestCase
from django.contrib.auth.models import Group
from ..models import *
from datetime import date


class CustomerFactoryTest(TestCase):
    """
    Test case for CustomerManager
    """

    def setUp (self):
        self.customer_group = Group.objects.create(name = 'Customer')
        self.customer = Customer.objects.create_customer(first_name = 'Test',
                                                         last_name= 'Customer',
                                                         email = 'test@domain.com',
                                                         acct = 11111,
                                                         password = 'password')

    def test_customer_attrs (self):
        self.assertEqual(self.customer.name, "Test Customer")
        self.assertEqual(self.customer.email, "test@domain.com")
        self.assertEqual(self.customer.acct, 11111)
        self.assertEqual(self.customer.createdate, date.today())
        self.assertEqual(self.customer.notes, "notes")
        self.assertEqual(self.customer.status, 1)


class ItemShipmentFactoryTest(TestCase):
    """
    Test case for InventoryManager and ShipmentManager
    """

    def setUp (self):
        self.customer_group = Group.objects.create(name = 'Customer')
        self.customer = Customer.objects.create_customer(first_name = 'Test',
                                                         last_name = 'Customer',
                                                         email = 'test@domain.com',
                                                         acct = 11111,
                                                         password = 'password')
        self.shipment = Shipment.objects.create_shipment(owner = self.customer,
                                                         palletized = True,
                                                         labor_time = 60,
                                                         notes = "notes",
                                                         tracking_number = 1234567890)
        self.item = Inventory.objects.create_inventory(shipset = self.shipment,
                                                       length = 5.0,
                                                       width = 5.0,
                                                       height = 5.0)

    def test_shipment_attrs (self):
        self.assertEqual(self.shipment.shipid, Shipment.objects.count())
        self.assertEqual(self.shipment.arrival, date.today())
        self.assertEqual(self.shipment.status, 0)
        self.assertEqual(self.shipment.owner, self.customer)
        self.assertEqual(self.shipment.palletized, True)
        self.assertEqual(self.shipment.labor_time, 60)
        self.assertEqual(self.shipment.status, 0)
        self.assertEqual(self.shipment.notes, "notes")
        self.assertEqual(self.shipment.tracking_number, 1234567890)

    def test_item_attrs (self):
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

    def test_shipment_ops (self):
        ship_ops = list(self.shipment.operations.all())
        self.assertEqual(self.shipment.status, len(ship_ops) - 1)
        self.assertEqual(self.shipment.get_status_display(), int(ship_ops[-1].op_code))

    def test_item_ops (self):
        item_ops = list(self.item.operations.all())
        self.assertEqual(self.item.status, len(item_ops) - 1)
        self.assertEqual(self.item.get_status_display(), int(item_ops[-1].op_code))

    def test_shipment_audit_log_entry(self):
        ship_audit_log_entries = self.shipment.audit_log.count()
        self.assertEqual(ship_audit_log_entries, 1)

    def test_inventory_audit_log_entry(self):
        for item in self.shipment.inventory.all():
            assert isinstance(item, Inventory)
            item_audit_log_entries = item.audit_log.count()
            self.assertEqual(item_audit_log_entries, 1)