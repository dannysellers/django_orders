"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Customer, Inventory, Operation
from datetime import date

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


# class CustomerTest(TestCase):
#     testcustomers = [
#         {'names': 'George Washington',
#          'acct': 48291,
#          'createdate': '2014-01-30'}
#     ]
#     def add_customer(self):
