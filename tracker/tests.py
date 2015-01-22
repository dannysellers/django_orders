"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *


# class SimpleTest(TestCase):
# 	def test_basic_addition (self):
# 		"""
# 		Tests that 1 + 1 always equals 2.
# 		"""
# 		self.assertEqual(1 + 1, 2)


class ItemOpTest(TestCase):
	def setUp(self):
		self.itemlist = Inventory.objects.all()

	def test_item_op_equality(self):
		"""
		Tests that each Inventory object has the correct number
		of ItemOperation objects associated with it.
		"""
		for item in self.itemlist:
			iocount = ItemOperation.objects.filter(item = item).count() + 1
			self.assertEqual(item.status, iocount)