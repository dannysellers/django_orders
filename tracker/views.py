from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Customer, Inventory, Operation
import forms


def encode_url (url):
	return url.replace(' ', '_')


def decode_url (url):
	return url.replace('_', ' ')


def index (request):
	context = RequestContext(request)
	context_dict = {}

	return render_to_response('tracker/index.html', context_dict, context)


def about (request):
	context = RequestContext(request)
	context_dict = {'name': 'About'}

	return render_to_response('tracker/about.html', context_dict, context)


def accounts (request):
	context = RequestContext(request)
	context_dict = {}

	try:
		# only display accounts whose status is 1 (active)
		customer_list = Customer.objects.order_by('acct').filter(status__exact=1)[:10]

		# header_list = Customer._meta.get_all_field_names()
		header_list = ['Account', 'Name']
		context_dict['headers'] = header_list

		# Replace spaces with underscores to retrieve URL
		for customer in customer_list:
			customer.url = encode_url(customer.name)

		context_dict['customer_list'] = customer_list

	except Customer.DoesNotExist:
		context_dict['error_message'] = "No accounts found."

	return render_to_response('tracker/accounts.html', context_dict, context)


def account_page (request, account_name_url):
	context = RequestContext(request)

	# Change underscores in the account name to spaces
	# The URL will have an underscore, which replaced
	# with a space corresponds to the customer
	account_name = encode_url(account_name_url)
	context_dict = {'account_name': account_name,
					'account_name_url': account_name_url}

	context_dict['headers'] = ['Name', 'Account', 'Email']

	try:
		_customer = Customer.objects.get(name__iexact = account_name)
		context_dict['customer'] = _customer

		context_dict['account_acct'] = _customer.acct
		context_dict['account_email'] = _customer.email

	except Customer.DoesNotExist:
		context_dict['error_message'] = "Sorry, I couldn't find that account."

	return render_to_response('tracker/accounts.html', context_dict, context)


def add_account (request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		form = forms.CustomerForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			print("Acct added: {} -- {}".format(form.acct, 
form.name))

			return index(request)
		else:
			print form.errors
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	return render_to_response('tracker/add_account.html', context_dict, context)


def remove_account(request, account_name_url):
	"""	Method to 'remove' an account (really just deactivating it)
	This isn't right--I copied from the add_account, but I'm not sure
	it'll actually need a form... """
	context = RequestContext(request)

	account_name = encode_url(account_name_url)
	context_dict = {'account_name': account_name,
					'account_name_url': account_name_url}

	if request.method == 'POST':
		_customer = Customer.objects.get(name__iexact=context_dict['account_name'])
		_customer.status = 0
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	return render_to_response('tracker/accounts.html', context_dict, context)


def add_item (request, account_name_url):
	print account_name_url
	return HttpResponse("This page is for adding items to a customer's inventory.")


def inventory (request):
	context = RequestContext(request)
	context_dict = {}
	context_dict['name'] = 'All Inventory'

	inventory_list = Inventory.objects.all().filter(status = 1)
	if inventory_list:
		context_dict['inventory_list'] = inventory_list
	else:
		context_dict['error_message'] = "No items found."

	return render_to_response('tracker/inventory.html', context_dict, context)
