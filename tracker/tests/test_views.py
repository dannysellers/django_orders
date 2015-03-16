from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from ..models import *
from datetime import date
from random import randint


class InventoryViewTests(TestCase):
    """
    Test case for views related to Inventory
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

    def test_inventory_list_view(self):
        url = reverse('inventory', 'tracker.urls')
        req = self.client.get(url)
        self.assertEqual(req.status_code, 200)
        self.assertTemplateUsed(req, 'tracker/inventory.html')
        self.assertIn(self.customer.name, req.content)
        for item in self.shipment.inventory_set.all():
            self.assertIn('/inventory?item={}'.format(item.itemid),
                          req.content)
        self.assertIn(reverse('shipment', kwargs = {'shipid': self.shipment.shipid}),
                      req.content)
        self.assertIn(reverse('account_page', kwargs = {'account_id': self.customer.acct}),
                      req.content)

    def test_inventory_detail_view(self):
        for item in self.shipment.inventory_set.all():
            url = '/inventory?item={}'.format(item.itemid)
            req = self.client.get(url)
            self.assertEqual(req.status_code, 200)
            self.assertTemplateUsed(req, 'tracker/inventory.html')
            self.assertIn(self.customer.name, req.content)
            self.assertIn(reverse('account_page', kwargs = {'account_id': self.customer.acct}),
                          req.content)
            self.assertIn(reverse('shipment', kwargs = {'shipid': self.shipment.shipid}),
                          req.content)

    # def test_inventory_status_view(self):
    #     from ..models import INVENTORY_STATUS_CODES
    #     for status in INVENTORY_STATUS_CODES:
    #         url = '/inventory?status={}'.format(status[0])
    #         req = self.client.get(url)