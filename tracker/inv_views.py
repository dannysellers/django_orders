from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import date

from models import Customer, Inventory
import forms


def get_items_by_status(status_bound):
	"""
	Creates a list of inventory items that have not yet reached status_bound
	(i.e. are not yet shipped, or whose orders are still in progresss).

	INVENTORY_STATUS_CODES = (
		('0', 'inventory_received'),
		('1', 'order_received'),
		('2', 'order_begun'),
		('3', 'order_completed'),
		('4', 'shipped'),
	)
	"""
	status = 0
	itemlist = []
	while status < status_bound:
		itemlist.append(Inventory.objects.get(status = status))
		status += 1

	return itemlist


def inventory(request):
	context = RequestContext(request)
	context_dict = {}
	# acct = request.GET.get('acct')
	status_filter = request.GET.get('status')

	try:
		# Retrieve one account's items
		# if acct:
		# 	try:
		# 		customer = Customer.objects.get(acct = acct)
		# 		context_dict['customer'] = customer
		# 		context_dict['inventory_list'] = Inventory.objects.get(owner = customer)
		# 	except Customer.DoesNotExist:
		# 		context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
		# 		return render_to_response('tracker/inventory.html', context_dict, context)
		# # Retrieve items with status below status_filter
		# elif status_filter:
		# 	context_dict['filter'] = status_filter
		# 	if status_filter == 'received':
		# 		context_dict['inventory_list'] = get_items_by_status(3)
		# 	elif status_filter == 'stored':
		# 		context_dict['inventory_list'] = get_items_by_status(4)
		# else:
		# 	context_dict['inventory_list'] = get_items_by_status(4)
		context_dict['filter'] = status_filter
		context_dict['inventory_list'] = get_items_by_status(3)
	except Inventory.DoesNotExist:
		context_dict['error_message'] = "No inventory found."

	return render_to_response('tracker/inventory.html', context_dict, context)


def add_item (request, account_name_url):
	# context = RequestContext(request)
	print account_name_url
	return HttpResponse("This page is for adding items to a customer's inventory.")