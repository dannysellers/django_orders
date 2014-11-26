from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from datetime import date

from models import Customer, Inventory
import utils
import forms


def inventory(request):
	context = RequestContext(request)
	context_dict = {}

	# URL keywords
	acct = request.GET.get('acct')
	status_filter = request.GET.get('status')
	# add = request.GET.get('add')
	# status_filter = code_to_status_int('Inventory', request.GET.get('status'))  # WIP

	context_dict['headers'] = ['ID', 'Owner', 'Quantity', 'Volume',
							   'Storage Fees', 'Status', 'Arrival']

	try:
		if acct:  # retrieve inventory by account
			try:
				acct = int(acct)
				customer = Customer.objects.get(acct = acct)
				context_dict['customer'] = customer
				inventory_list = Inventory.objects.order_by('itemid').filter(
					owner = customer)
				context_dict['inventory_list'] = inventory_list

				_date = date.today()
				context_dict['date'] = _date
				context_dict['storage_fees'] = utils.calc_storage_fees(inventory_list, _date)[0]
			except Customer.DoesNotExist:
				context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
				return render_to_response('tracker/inventory.html', context_dict, context)
			except Inventory.DoesNotExist:
				context_dict['error_message'] = "No inventory found."
				return render_to_response('tracker/inventory.html', context_dict, context)

		elif status_filter:
			if status_filter == 'stored':  # retrieve all but shipped (4)
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
			context_dict['inventory_list'] = inventory_list

		else:
			context_dict['filter'] = 'All'
			ilist = Inventory.objects.all()
			context_dict['inventory_list'] = ilist

	except Inventory.DoesNotExist:
		context_dict['inventory_list'] = []
		context_dict['error_message'] = "No inventory found."

	return render_to_response('tracker/inventory.html', context_dict, context)


def add_item (request, account_name_url):
	"""
	Form to add item. Intended behavior: Either receive account # within
	URL, or allow for selection of customer if no param is passed
	"""
	context = RequestContext(request)
	context_dict = {}

	owner = account_name_url

	if request.method == 'POST':
		form = forms.InventoryForm(request.POST)

		if form.is_valid():
			item = form.save(commit = False)

			try:
				cust = Customer.objects.get(acct = owner)
				item.owner = cust
			except Customer.DoesNotExist:
				return render_to_response('tracker/add_customer.html',
										  context_dict,
										  context)

			item.volume = item.length * item.width * item.height
			item.storage_fees = item.quantity * item.volume
			item.save()

			return redirect(inventory, permanent=True)
		else:
			print form.errors
	else:
		form = forms.InventoryForm()

	context_dict['form'] = form
	context_dict['owner'] = owner
	return render_to_response('tracker/add_item.html', context_dict, context)