from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from datetime import date

from models import Customer, Inventory
# import utils
import forms


def inventory(request):
	context = RequestContext(request)
	context_dict = {}

	# URL keywords
	acct = request.GET.get('acct')
	status_filter = request.GET.get('status')
	storage_fees = request.GET.get('storage_fees')
	# add = request.GET.get('add')
	# status_filter = code_to_status_int('Inventory', request.GET.get('status'))  # WIP

	context_dict['headers'] = ['ID', 'Owner', 'Quantity', 'Volume (ft.^3)',
							   'Storage Fees', 'Status', 'Arrival']

	try:
		if acct:  # Retrieve inventory by account
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
				# context_dict['storage_fees'] = utils.calc_storage_fees(inventory_list, _date)[0]

			except Customer.DoesNotExist:
				context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
				return render_to_response('tracker/inventory.html', context_dict, context)
			except Inventory.DoesNotExist:
				context_dict['error_message'] = "No inventory found."
				return render_to_response('tracker/inventory.html', context_dict, context)

		elif status_filter:  # Retrieve inventory by status
			if status_filter == 'stored':  # Retrieve all but shipped (4)
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

			# for item in inventory_list:
			# 	item.owner.url = '/accounts/' + str(item.owner.acct)

		elif storage_fees:  # Retrieve items currently incurring storage fees
			context_dict['filter'] = 'Currently incurring storage fees'
			inventory_list = []
			for item in Inventory.objects.all():
				if abs((item.arrival - date.today()).days) > 7:
					inventory_list.append(item)

		else:
			context_dict['filter'] = 'All'
			inventory_list = Inventory.objects.all()

		context_dict['inventory_list'] = inventory_list

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

		if form.is_valid():
			item = form.save(commit = False)

			try:
				cust = Customer.objects.get(acct = owner)
				item.owner = cust

				item.length = form.cleaned_data['length'] / 12  # storage fees are per ft^3
				item.width = form.cleaned_data['width'] / 12
				item.height = form.cleaned_data['height'] / 12
				# item.length = form.length / 12
				# item.width = form.width / 12
				# item.height = form.height / 12
				item.volume = item.length * item.width * item.height
				item.storage_fees = item.quantity * item.volume
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