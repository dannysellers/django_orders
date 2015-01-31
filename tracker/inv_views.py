from datetime import date, datetime

# try:
# 	from django.utils import timezone as datetime
# except ImportError:
# 	from datetime import datetime as datetime

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import *
import utils
import forms
import re


@cache_control(no_cache = True)
def inventory (request):
	context = RequestContext(request)
	context_dict = {}

	# URL keywords
	acct = request.GET.get('acct')
	status_filter = request.GET.get('status')
	storage_fee_arg = request.GET.get('storage_fees')
	item = request.GET.get('item')

	header_list = ['Ship ID', 'Item ID', 'Owner', 'Total Volume (ft.^3)',
				   'Storage Fees', 'Status', 'Arrival']

	try:
		if acct or status_filter or storage_fee_arg:
			context_filter = []
			# TODO: Add gui method to chain queries
			try:
				inventory_list = Inventory.objects.all()
			except Inventory.DoesNotExist:
				context_dict['error_message'] = "No inventory found."
				return render_to_response('tracker/inventory.html', context_dict, context)

			if acct:
				try:
					acct = int(acct)
					customer = Customer.objects.get(acct = acct)
					context_dict['customer'] = customer
					context_filter.append(str(customer))
					inventory_list = inventory_list.filter(shipset__owner = customer)
					if not inventory_list:
						if int(customer.status) == 0:
							messages.add_message(request, messages.INFO, "This account is inactive.")
						else:
							messages.add_message(request, messages.INFO, "This customer has no items.")

					_date = date.today()
					context_dict['date'] = _date

				except Customer.DoesNotExist:
					context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
					return render_to_response('tracker/inventory.html', context_dict, context)

			if status_filter:
				if status_filter == 'inducted':
					inventory_list = inventory_list.filter(status = 0)
					context_filter.append('Inducted')
				elif status_filter == 'stored':  # Retrieve all but shipped (4)
					inventory_list = inventory_list.exclude(status = 4)
					context_filter.append('Stored')
				elif 'order' in status_filter:
					_context = 'Order'
					if 'received' in status_filter:  # 1
						inventory_list = inventory_list.filter(status = 1)
						_context += ' received'
					elif 'begun' in status_filter:  # 2
						inventory_list = inventory_list.filter(status = 2)
						_context += ' begun'
					elif 'completed' in status_filter:  # 3
						inventory_list = inventory_list.filter(status = 3)
						_context += ' completed (not yet shipped)'
					context_filter.append(_context)
				elif status_filter == 'all':
					context_dict['b_inactive'] = '_'
					context_filter.append('All')
					header_list.append('Departure')
				else:
					messages.add_message(request, messages.INFO, """I didn't recognize status filter '{}'.
					You can use: <i>inducted</i>, <i>stored</i>, <i>order_received</i>, <i>order_begun,</i>
					<i>order_completed</i>, or <i>all</i> as possible filters.""".format(status_filter))
					context_filter.append('All')
					header_list.append('Ship Date')
			else:
				inventory_list = inventory_list.exclude(status = 4)  # otherwise only show stored items
				context_filter.append('Stored')

			if storage_fee_arg:
				_filtered_list = []
				if storage_fee_arg.lower() == 'no':
					# TODO: How to use True / False as values, rather than yes/no
					context_filter.append('Items not yet incurring storage fees')
					for item in inventory_list.exclude(status = 4):
						if abs((item.shipset.arrival - date.today()).days) < 7:
							_filtered_list.append(item)
				else:
					context_filter.append('Currently incurring storage fees')
					for item in inventory_list.exclude(status = 4):
						if abs((item.shipset.arrival - date.today()).days) >= 7:
							_filtered_list.append(item)

				inventory_list = _filtered_list

			if len(context_filter) > 1:
				context_dict['filter'] = ' > '.join(context_filter)
			else:
				context_dict['filter'] = context_filter[0]  # still gets passed a list

			storage_fees = utils.calc_storage_fees(inventory_list)

		# Retrieve specific item and its history
		elif item:
			_item = Inventory.objects.get(itemid = item)
			context_dict['item'] = _item
			customer = Customer.objects.get(acct = _item.shipset.owner.acct)
			context_dict['customer'] = customer

			op_headers = ['Op ID', 'Op Code', 'Time', 'User']
			context_dict['op_headers'] = op_headers
			context_dict['op_list'] = ItemOperation.objects.all().filter(item = _item)

			storage_fees = utils.calc_storage_fees(_item)

			# for the sake of the template
			inventory_list = []

		else:
			context_dict['filter'] = 'All'
			inventory_list = Inventory.objects.all()
			storage_fees = utils.calc_storage_fees(inventory_list.exclude(status = 4))
			context_dict['b_inactive'] = '_'
			header_list.append('Departure')

		if len(inventory_list) > 0:
			context_dict['count'] = str(len(inventory_list))

		context_dict['headers'] = header_list
		context_dict['storage_fees'] = storage_fees

		# Pagination
		page_items = request.GET.get('items')
		page = request.GET.get('page')

		if not page_items:
			page_items = 25
		if not page:
			page = 1

		paginator = Paginator(inventory_list, page_items, orphans = 5)

		try:
			inventory_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver the first page
			inventory_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver the last page
			inventory_list = paginator.page(paginator.num_pages)

		context_dict['inventory_list'] = inventory_list

		# Preserve all GET params
		params = []
		for key, value in request.GET.iteritems():
			params.append("&{}={}".format(key, value))

		# The first char is a &, which we replace with a ?
		params = '?' + ''.join(params)[1:]

		# Only change the page number
		if inventory_list.has_previous():
			context_dict['prev_page_url'] = re.sub('page=(\d+)', 'page=' + str(inventory_list.previous_page_number()), params)
		if inventory_list.has_next():
			context_dict['next_page_url'] = re.sub('page=(\d+)', 'page=' + str(inventory_list.next_page_number()), params)

	except Inventory.DoesNotExist:
		context_dict['inventory_list'] = []
		context_dict['error_message'] = "No items found in database."

	return render_to_response('tracker/inventory.html', context_dict, context)


@login_required
def add_item (request, account_url):
	"""
	Form to add item. Intended behavior: Either receive account # within
	URL, or allow for selection of customer if no param is passed
	"""
	# TODO: This needs updating / may not be relevant any more given shipments

	context = RequestContext(request)
	context_dict = {}

	try:
		owner = Customer.objects.get(acct = account_url)
	except Customer.DoesNotExist:
		messages.add_message(request, messages.ERROR, "Customer {} not found.".format(account_url))
		return render_to_response('tracker/add_customer.html',
								  context_dict,
								  context)

	if request.method == 'POST':
		form = forms.InventoryForm(request.POST)

		if form.is_valid():
			item = form.save(commit = False)

			item.owner = owner

			item.length = form.cleaned_data['length'] / 12
			item.width = form.cleaned_data['width'] / 12
			item.height = form.cleaned_data['height'] / 12
			item.save({'user': request.user})

			return HttpResponseRedirect('/inventory?acct={}'.format(owner.acct))

		else:
			print form.errors
	else:
		form = forms.InventoryForm()

	context_dict['form'] = form
	context_dict['owner'] = owner
	context_dict['form_type'] = 'item'
	return render_to_response('tracker/form.html', context_dict, context)


@login_required
def change_item_status (request):
	"""
	Receives list of checked items, passes them to item manager page
	If /change_status?item=##### , manage individual item.
	If /manage_items/, receive list of items.
	"""
	itemlist = []

	if request.method == 'POST':
		if request.GET.get('item'):  # individual item passed as URL param
			_itemid = request.GET.get('item')
			try:
				item = Inventory.objects.get(itemid = _itemid)
				itemlist.append(item)
			except Inventory.DoesNotExist:
				print("Item {} could not be found".format(_itemid))

		# Recover operation and labor_time vals, and list of items if applicable
		for key, value in request.POST.iteritems():
			if value == 'on':  # multiple items; checked checkboxes return 'on'
				try:
					item = Inventory.objects.get(itemid = key)
					itemlist.append(item)
				except Inventory.DoesNotExist:
					print("Item {} could not be found".format(key))
			if key == 'operation':  # retrieve value of desired op
				operation = value

		for item in itemlist:
			item.status = operation

			item.save({'user': request.user})

		if len(itemlist) == 1:
			return HttpResponseRedirect('/inventory?item={}'.format(itemlist[0].itemid))
		else:
			return HttpResponseRedirect('/inventory?acct={}'.format(itemlist[0].owner.acct))
	else:
		messages.add_message(request, messages.ERROR, """No request was passed.
				Try visiting this page from a <a href="/inventory?status=stored">customer's inventory (e.g.
				/inventory?acct=#####)</a>.""")

		return HttpResponseRedirect('/inventory?status=stored')