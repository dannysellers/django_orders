from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from datetime import date, datetime
from django.contrib import messages
from json import dumps

from models import Customer, Inventory, Operation
import utils
import forms


def inventory(request):
	context = RequestContext(request)
	context_dict = {}

	# URL keywords
	acct = request.GET.get('acct')
	status_filter = request.GET.get('status')
	storage_fee_arg = request.GET.get('storage_fees')
	item = request.GET.get('item')
	add = request.GET.get('add')

	header_list = ['ID', 'Owner', '# of Cartons', 'Total Volume (ft.^3)',
							   'Storage Fees', 'Status', 'Arrival']

	try:
		if acct or status_filter or storage_fee_arg:
			# TODO: Add visual confirmation of chained queries
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
					customer = Customer.objects.get(acct=acct)
					context_dict['customer'] = customer
					context_filter.append(str(customer))
					inventory_list = inventory_list.filter(owner=customer)
					if not inventory_list:
						messages.add_message(request, messages.INFO, "This customer has no items.")

					_date = date.today()
					context_dict['date'] = _date
					header_list.insert(0, ' ')

				except Customer.DoesNotExist:
					context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
					return render_to_response('tracker/inventory.html', context_dict, context)

			if status_filter:
				if status_filter == 'inducted':
					inventory_list = inventory_list.filter(status=0)
					context_filter.append('Inducted')
				elif status_filter == 'stored':  # Retrieve all but shipped (4)
					inventory_list = inventory_list.exclude(status=4)
					context_filter.append('Stored')
				elif 'order' in status_filter:
					_context = 'Order'
					if 'received' in status_filter:  # 1
						inventory_list = inventory_list.filter(status=1)
						_context += ' received'
					elif 'begun' in status_filter:  # 2
						inventory_list = inventory_list.filter(status=2)
						_context += ' begun'
					elif 'completed' in status_filter:  # 3
						inventory_list = inventory_list.filter(status=3)
						_context += ' completed (not yet shipped)'
					context_filter.append(_context)
				else:
					context_filter.append('All')
					header_list.append('Ship Date')
			else:
				inventory_list = inventory_list.exclude(status=4)  # otherwise only show stored items
				context_filter.append('Stored')

			if storage_fee_arg:
				_filtered_list = []
				if storage_fee_arg.lower() == 'no':
					# TODO: How to use True / False as values, rather than yes/no
					context_filter.append('Items not yet incurring storage fees')
					for item in inventory_list.exclude(status=4):
						if abs((item.arrival - date.today()).days) < 7:
							_filtered_list.append(item)
				else:
					context_filter.append('Currently incurring storage fees')
					for item in inventory_list.exclude(status=4):
						if abs((item.arrival - date.today()).days) >= 7:
							_filtered_list.append(item)

				inventory_list = _filtered_list

			if len(context_filter) > 1:
				context_dict['filter'] = ' > '.join(context_filter)
			else:
				context_dict['filter'] = context_filter[0]  # still gets passed a list

			storage_fees = utils.calc_storage_fees(inventory_list)

		# Retrieve specific item and its history
		elif item:
			_item = Inventory.objects.get(itemid=item)
			context_dict['item'] = _item
			customer = Customer.objects.get(acct=_item.owner.acct)
			context_dict['customer'] = customer

			op_headers = ['Op ID', 'Op Code', 'Start', 'Finish', 'Labor Time (mins)']
			context_dict['op_headers'] = op_headers
			context_dict['op_list'] = Operation.objects.all().filter(item=_item)

			storage_fees = utils.calc_storage_fees(_item)

			# for the sake of the template
			inventory_list = []

		else:
			context_dict['filter'] = 'All'
			inventory_list = Inventory.objects.all()
			storage_fees = utils.calc_storage_fees(inventory_list.exclude(status=4))

		context_dict['inventory_list'] = inventory_list
		context_dict['count'] = str(len(inventory_list))
		context_dict['headers'] = header_list
		context_dict['storage_fees'] = storage_fees

	except Inventory.DoesNotExist:
		context_dict['inventory_list'] = []
		context_dict['error_message'] = "No items found in database."

	return render_to_response('tracker/inventory.html', context_dict, context)


def add_item (request, account_url):
	"""
	Form to add item. Intended behavior: Either receive account # within
	URL, or allow for selection of customer if no param is passed
	"""
	context = RequestContext(request)
	context_dict = {}

	owner = account_url

	if request.method == 'POST':
		form = forms.InventoryForm(request.POST)
		form.itemid = len(Inventory.objects.all())

		if form.is_valid():
			item = form.save(commit = False)

			try:
				cust = Customer.objects.get(acct = owner)
				item.owner = cust

				item.itemid = len(Inventory.objects.all())
				item.length = form.length / 12  # storage fees are per ft^3
				item.width = form.width / 12
				item.height = form.height / 12
				item.volume = form.length * form.width * form.height
				item.storage_fees = form.quantity * form.volume
				item.save()
			except Customer.DoesNotExist:
				return render_to_response('tracker/add_customer.html',
										  context_dict,
										  context)

			return redirect(inventory)
		else:

			print form.errors
	else:
		form = forms.InventoryForm()

	context_dict['form'] = form
	context_dict['owner'] = owner
	return render_to_response('tracker/add_item.html', context_dict, context)

# def add_item(request, account_url):
# 	if request.method == 'POST':
# 		form = forms.ItemForm(request.POST)
# 		if form.is_valid:
# 			# Process data from form.cleaned_data
# 			return HttpResponseRedirect('')


def change_item_status(request):
	"""
	Receives list of checked items, passes them to item manager page
	If /change_status?item=##### , manage individual item.
	If /manage_items/, receive list of items.
	"""
	# TODO: Integrate this with individual item page
	# TODO: Enforce only one copy of induction / shipment per item
	# TODO: Enforce triplets of order received, started, done
	context = RequestContext(request)
	itemlist = []

	""" Prepare itemlist for processing by db / parsing to json """
	if request.GET.get('item'):  # individual item passed as URL param
		_itemid = request.GET.get('item')
		try:
			item = Inventory.objects.get(itemid=_itemid)
			itemlist.append(item)
		except Inventory.DoesNotExist:
			print("Item {} could not be found".format(_itemid))

	# Recover operation and labor_time vals, and list of items if applicable
	for key, value in request.POST.iteritems():
		if value == 'on':  # multiple items; checked checkboxes return 'on'
			try:
				item = Inventory.objects.get(itemid=key)
				itemlist.append(item)
			except Inventory.DoesNotExist:
				print("Item {} could not be found".format(key))
		if key == 'operation':  # retrieve value of desired op
			operation = value
		if key == 'labor_time':
			labor_time = int(value)

	""" Assign new operation to each item """
	if request.method == 'POST':
		op_list = []
		for item in itemlist:
			item.status = operation
			td = datetime.today()

			# TODO: Doesn't handle adding minutes very well...
			mins = labor_time % 60
			hrs = int(labor_time / 60)
			td2 = datetime(td.year, td.month, td.day, td.hour + hrs, (td.minute + mins) % 60, 0, 0)

			o = Operation.objects.get_or_create(item=item, start=datetime.now(),
												finish=td2, labor_time=labor_time,
												op_code = operation)[0]
			item.save()

			# for op in list(Operation.objects.all().filter(item = item)):
			# 	op_list.append({
			# 		"op_id": op.id,
			# 		"op_code": op.op_code,
			# 		"start": op.start,
			# 		"finish": op.finish,
			# 		"labor_time": op.labor_time
			# 	})
		# return HttpResponse(dumps(op_list, indent=4), content_type='application/json')
	else:
		message = """No request was passed.
		Try visiting this page from a <a href="/inventory?status=stored">customer's inventory (e.g. /inventory?acct=#####)</a>."""

		# TODO: use messages framework to pass the above text
		return HttpResponseRedirect('/inventory?status=stored')