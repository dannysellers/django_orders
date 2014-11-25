from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from datetime import date

from models import Customer, Inventory
from utils import int_to_status_code, code_to_status_int
import forms


def inventory(request):
	context = RequestContext(request)
	context_dict = {}

	# URL keywords
	acct = request.GET.get('acct')
	# status_filter = int(request.GET.get('status'))
	# status_filter = code_to_status_int('Inventory', request.GET.get('status'))  # WIP

	context_dict['headers'] = ['ID', 'Owner', 'Quantity', 'Volume', 'Storage Fees', 'Status']

	try:
		if acct:
			try:
				acct = int(acct)
				customer = Customer.objects.get(acct = acct)
				context_dict['customer'] = customer
				context_dict['inventory_list'] = Inventory.objects.order_by('itemid').filter(
					owner = customer)
				pass
			except Customer.DoesNotExist:
				context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(acct)
				return render_to_response('tracker/inventory.html', context_dict, context)
			except Inventory.DoesNotExist:
				context_dict['error_message'] = "No inventory found."
				return render_to_response('tracker/inventory.html', context_dict, context)

		# elif status_filter:
		# 	item_list = []
			# assert isinstance(status_filter, int)
			# for i in range(0, status_filter):
			# 	for item in Inventory.objects.all().filter(status = i):
			# 		item_list.append(item)
			# context_dict['inventory_list'] = item_list

		else:
			context_dict['filter'] = 'All'
			ilist = Inventory.objects.all()
			context_dict['inventory_list'] = ilist

	except Inventory.DoesNotExist:
		context_dict['inventory_list'] = []
		context_dict['error_message'] = "No inventory found."

	return render_to_response('tracker/inventory.html', context_dict, context)


def add_item (request, account_name_url):
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
	return render_to_response('tracker/add_item.html', context_dict, context)