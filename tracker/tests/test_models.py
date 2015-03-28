from django.test import TestCase
from django.contrib.auth.models import Group
from ..models import *
from random import randint
from datetime import date, timedelta


class CustomerMethodTest(TestCase):
    """
    Test case for methods of Customer model
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
                                                         notes = "Test notes",
                                                         tracking_number = 12345)
        for i in range(randint(1, 5)):
            Inventory.objects.create_inventory(shipset = self.shipment,
                                               length = randint(1.0, 5.0),
                                               width = randint(1.0, 5.0),
                                               height = randint(1.0, 5.0))

    def test_customer_name (self):
        self.assertEqual(self.customer.name, "{} {}".format(
            self.customer.first_name,
            self.customer.last_name
        ))

    def test_customer_storage_fees (self):
        _fees = 0.00
        for item in self.customer.inventory.exclude(status = 4):
            _fees += item.get_storage_fees()
        self.assertEqual(self.customer.storage_fees, _fees)

    def test_customer_close_account (self):
        today = date.today()
        self.customer.close_account()
        self.assertEqual(self.customer.status, 0)
        self.assertEqual(self.customer.closedate, today)


class ShipmentMethodTest(TestCase):
    """
    Test case for methods of Shipment model
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
                                                         notes = "Test notes",
                                                         tracking_number = 12345)
        for i in range(randint(1, 5)):
            Inventory.objects.create_inventory(shipset = self.shipment,
                                               length = randint(1.0, 5.0),
                                               width = randint(1.0, 5.0),
                                               height = randint(1.0, 5.0))

    def test_shipment_storage_fees (self):
        _fees = 0.00
        for item in self.shipment.inventory.exclude(status = 4):
            _fees += item.get_storage_fees()
        self.assertEqual(self.shipment.storage_fees, _fees)
        # self.assertListEqual(self.shipment.inventory.all(),
        #     self.shipment.inventory.exclude(status = 4))

    def test_shipment_set_status (self):
        self.assertEqual(self.shipment.status, 0)
        for item in self.shipment.inventory.all():
            self.assertEqual(item.status, '0')

        self.shipment.set_status(1)
        self.assertEqual(self.shipment.status, 1)
        for item in self.shipment.inventory.all():
            self.assertEqual(item.status, '1')


class InventoryMethodTest(TestCase):
    """
    Test case for methods of Inventory model
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
                                                         notes = "Test notes",
                                                         tracking_number = 12345)
        for i in range(randint(1, 5)):
            Inventory.objects.create_inventory(shipset = self.shipment,
                                               length = randint(1.0, 5.0),
                                               width = randint(1.0, 5.0),
                                               height = randint(1.0, 5.0))

    def test_get_item_storage_fees (self):
        for item in self.shipment.inventory.all():
            if item.status != 4 and (date.today() - item.arrival).days >= 10:
                _fees = item.volume * UNIT_STORAGE_FEE
            else:
                _fees = 0.00
            self.assertEqual(item.get_storage_fees(), _fees)

    def test_get_item_total_fees_incurred (self):
        self.shipment.set_status(4)
        for item in self.shipment.inventory.all():
            # TODO: Settle how to create shipments in the past (that incur storage fees)
            days_in_paid_storage = (item.departure - item.arrival).days  # - 10
            self.assertEqual(item.get_storage_fees(), days_in_paid_storage * item.storage_fees)