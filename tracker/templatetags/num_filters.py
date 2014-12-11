from django import template

register = template.Library()


@register.filter
def length(value, arg):
	"""	Receives long number, truncates it to length of arg """
	_length = int(arg)
	_string = str(value).split('.')  # truncate only values after the decimal
	if _string[1] == '0':
		_string[1] = '00'
	return _string[0] + '.' + _string[1][:_length]


@register.filter
def op_code(value):
	""" Receives numerical operation code, returns status """
	value = int(value)
	if value == 0:
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