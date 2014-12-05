from models import Customer, Inventory
from decimal import Decimal, getcontext
from datetime import date


def int_to_status_code(cls, code):
	"""
	Takes class and status code, returns string associated with the code
	"""
	code = int(code)
	if cls == 'Customer':
		if code == 0:
			return 'Inactive'
		elif code == 1:
			return 'Active'
		else:
			raise TypeError('Status code not recognized')
	elif cls == 'Inventory':
		if code == 0:
			return 'Inventory received'
		elif code == 1:
			return 'Order received'
		elif code == 2:
			return 'Order started'
		elif code == 3:
			return 'Order completed'
		elif code == 4:
			return 'Item shipped'
		else:
			raise TypeError('Status code not recognized')
	else:
		raise TypeError('Class not recognized')


def code_to_status_int(cls, code):
	"""
	Takes status code name, returns integer
	"""
	code = str(code).lower()
	code.replace(' ', '_')

	if cls == 'Customer':
		if code == 'active':
			return 1
		elif code == 'inactive':
			return 0
		else:
			raise TypeError('Status string not recognized')
	elif cls == 'Inventory':
		if code == 'inducted':
			return 0
		elif 'received' in code:
			if 'inventory' in code:  # inventory received
				return 0
			elif 'order' in code:  # order received
				return 1
			else:
				raise TypeError('Status string not recognized')
		elif 'order' in code:
			if 'begun' in code or 'started' in code:
				return 2
			elif 'completed' in code:
				return 3
			else:
				raise TypeError('Status string not recognized')
		elif 'shipped' in code:
			return 4
		else:
				raise TypeError('Status string not recognized')
	else:
		raise TypeError('Class not recognized')


def calc_storage_fees(*args):
	"""
	Receives either a list of inventory items, or a customer account number;
	returns storage fee calculation
	"""
	_arg = args[0]  # args is a tuple
	if isinstance(_arg, int):
		customer = Customer.objects.get(acct=_arg)
		inventory_list = Inventory.objects.all().filter(owner=customer)
	elif isinstance(_arg, list):
		inventory_list = []
		for item in _arg:
			if isinstance(item, Inventory):
				item = Inventory.objects.get(itemid=item.itemid)
				inventory_list.append(item)
	else:
		inventory_list = []

	storage_fees = 0
	for item in inventory_list:
		if abs((item.arrival - date.today()).days) > 7:
					storage_fees += item.storage_fees

	return storage_fees