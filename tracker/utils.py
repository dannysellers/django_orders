# from models import Customer, Inventory


def int_to_status_code(cls, code):
	"""
	Takes class and status code, returns string associated with the code
	"""
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
			raise TypeError('Status code not recognized')
	elif cls == 'Inventory':
		pass
	else:
		raise TypeError('Class not recognized')