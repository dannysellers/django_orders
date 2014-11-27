from django import template

register = template.Library()


@register.filter
def length(value, arg):
	"""
	Receives long number, truncates it to length of arg
	"""
	_length = int(arg)
	_string = str(value).split('.')  # truncate only values after the decimal
	# if len(_string[0]) == 1:
	# 	_string[0] = '0' + _string[0]
	return _string[0] + '.' + _string[1][:_length]


@register.filter
def cost_length(value, arg):
	"""
	Receives long number, truncates and prepends $.
	This could probably be combined with the above filter...
	"""
	_length = int(arg)
	_string = str(value).split('.')
	return '$' + _string[0] + '.' + _string[1][:_length]