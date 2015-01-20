from django import template

register = template.Library()


@register.filter
def length (value, length):
	"""
	Receives `value`, truncates to length
	:param value: Value to truncate
	:param length: Length to truncate after the decimal
	:return:
	"""
	_length = int(length)
	_string = str(value).split('.')
	if len(_string[1]) == 1:  # Enforce at least two zeroes after the decimal
		_string[1] = '00'
	return _string[0] + '.' + _string[1][:_length]


@register.filter
def op_code (value):
	"""
	Converts numerical operation status value to string
	:param value: Item / Operation status
	:return: String status
	"""
	value = int(value)
	if not value:
		return 'Inducted'
	elif value == 0:
		return 'Inducted'
	elif value == 1:
		return 'Order received'
	elif value == 2:
		return 'Order started'
	elif value == 3:
		return 'Order completed'
	elif value == 4:
		return 'Shipped'
	else:
		return 'Unknown operation code ({})'.format(value)


@register.filter
def cust_status (value):
	"""
	Converts numerical customer status value to string
	:param value: Customer status
	:return: String status
	"""
	value = int(value)
	if value == 0:
		return 'Inactive'
	elif value == 1:
		return 'Active'
	elif not value:
		return 'No val received!'
	else:
		return 'Unknown status code ({})'.format(value)