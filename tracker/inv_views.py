from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from datetime import date

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
	# status_filter = code_to_status_int('Inventory', request.GET.get('status'))  # WIP

	header_list = ['ID', 'Owner', '# of Cartons', 'Total Volume (ft.^3)',
							   'Storage Fees', 'Status', 'Arrival']

	try:
		# Retrieve inventory by account
		if acct:
			try:
				acct = int(acct)
				customer = Customer.objects.get(acct = acct)
				context_dict['customer'] = customer
				inventory_list = Inventory.objects.order_by('itemid').filter(
					owner = customer).exclude(status=4)  # Show only stored items
				if not inventory_list:
					context_dict['message'] = "This customer has no items stored in inventory."

				_date = date.today()
				context_dict['date'] = _date
				header_list.insert(0, ' ')

				storage_fees = utils.calc_storage_fees(customer.acct)

			except Customer.DoesNotExist:
				context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
				return render_to_response('tracker/inventory.html', context_dict, context)
			except Inventory.DoesNotExist:
				context_dict['error_message'] = "No inventory found."
				return render_to_response('tracker/inventory.html', context_dict, context)

		# Retrieve inventory by status
		elif status_filter:
			if status_filter == 'inducted':
				inventory_list = Inventory.objects.all().filter(status=0)
				context_dict['filter'] = 'Inducted'
			elif status_filter == 'stored':  # Retrieve all but shipped (4)
				inventory_list = Inventory.objects.all().exclude(status=4)
				context_dict['filter'] = 'Stored'
			elif 'order' in status_filter:
				context_dict['filter'] = 'Order '
				if 'received' in status_filter:  # 1
					inventory_list = Inventory.objects.all().filter(status=1)
					context_dict['filter'] += 'received'
				elif 'begun' in status_filter:  # 2
					inventory_list = Inventory.objects.all().filter(status=2)
					context_dict['filter'] += 'begun'
				elif 'completed' in status_filter:  # 3
					inventory_list = Inventory.objects.all().filter(status=3)
					context_dict['filter'] += 'completed (not yet shipped)'
			else:
				inventory_list = Inventory.objects.all()
				context_dict['filter'] = 'All'

			storage_fees = utils.calc_storage_fees(inventory_list)

			# for item in inventory_list:
			# 	item.owner.url = '/accounts/' + str(item.owner.acct)

		# Retrieve items currently incurring storage fees
		elif storage_fee_arg:
			if storage_fee_arg.lower() != 'no':
				# TODO: How to use True / False as values, rather than yes/no
				context_dict['filter'] = 'Currently incurring storage fees'
				inventory_list = []
				for item in Inventory.objects.all().exclude(status=4):
					if abs((item.arrival - date.today()).days) >= 7:
						inventory_list.append(item)
			elif storage_fee_arg.lower() == 'no':
				context_dict['filter'] = 'Items not yet incurring storage fees'
				inventory_list = []
				for item in Inventory.objects.all().exclude(status=4):
					if abs((item.arrival - date.today()).days) < 7:
						inventory_list.append(item)

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

			return redirect(inventory, permanent=True)
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


def manage_items(request):
	"""
	Receives list of checked items, passes them to item manager page
	"""
	# TODO: Integrate this with individual item page
	# TODO: Enforce only one copy of induction / shipment per item
	# TODO: Enforce triplets of order received, started, done
	context = RequestContext(request)
	itemlist = []
	if request.GET.get('item'):  # individual item
		itemlist.append(request.GET.get('item'))

	for key, value in request.POST.iteritems():
		if value == 'on':  # multiple items; checked checkboxes return 'on'
			itemlist.append(Inventory.objects.get(itemid=key))
		if key == 'operation':  # retrieve value of desired op
			# TODO: Remove manual int/code conversion
			operation = utils.int_to_status_code('Inventory', value)
		if key == 'labor_time':
			labor_time = value

	if request.method == 'POST':
		return HttpResponse("""You're looking to change the status of {} items to {}.
		That operation took {} minutes.""".format(len(itemlist), operation, labor_time))
	else:
		message = """No request was passed.
		Try visiting this page from a <a href="/inventory?status=stored">customer's inventory (e.g. /inventory?acct=#####)</a>."""

		# TODO: use messages framework to pass the above text
		return HttpResponseRedirect('/inventory?status=stored')