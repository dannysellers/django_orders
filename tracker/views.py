from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import date
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Customer, Inventory
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
		customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)
		# paginator = Paginator(customer_list, 15)  # show 15 customers per page

		# page = request.GET.get('page')

		header_list = ['Account', 'Name']
		context_dict['headers'] = header_list

		# Replace spaces with underscores to retrieve URL
		for customer in customer_list:
			customer.url = encode_url(customer.name)

		context_dict['customer_list'] = customer_list

	except Customer.DoesNotExist:
		context_dict['error_message'] = "No accounts found."

	# try:
	# 	customers = paginator.page(page)
	# except PageNotAnInteger:
	# 	If page isn't an integer, deliver first page
		# customers = paginator.page(1)
	# except EmptyPage:
	# 	If page is out of range, deliver last page
	# 	customers = paginator.page(paginator.num_pages)

	# context_dict['customers'] = customers

	return render_to_response('tracker/accounts.html', context_dict, context)


def account_page (request, account_name_url):
	# TODO: Indicate status of account
	context = RequestContext(request)

	# Change underscores in the account name to spaces
	# The URL will have an underscore, which replaced
	# with a space corresponds to the customer
	account_name = decode_url(account_name_url)
	context_dict = dict(account_name = account_name, account_name_url = account_name_url)

	context_dict['headers'] = ['Account', 'Name', 'Email']

	try:
		_customer = Customer.objects.get(name__iexact = account_name)
		context_dict['customer'] = _customer

		context_dict['account_acct'] = _customer.acct
		context_dict['account_email'] = _customer.email

	except Customer.DoesNotExist:
		context_dict['error_message'] = "Sorry, I couldn't find {}'s account.".format(account_name)

	return render_to_response('tracker/accounts.html', context_dict, context)


def account_num_page (request, account_num_url):
	# TODO: Indicate status of account
	context = RequestContext(request)

	account_num = account_num_url
	context_dict = {'account_acct': account_num}

	context_dict['headers'] = ['Account', 'Name', 'Email']

	try:
		_customer = Customer.objects.get(acct__exact = account_num)
		context_dict['customer'] = _customer

		context_dict['account_name'] = _customer.name
		context_dict['account_email'] = _customer.email

	except Customer.DoesNotExist:
		context_dict['error_message'] = "Sorry, I couldn't find account #{}.".format(account_num)

	return render_to_response('tracker/accounts.html', context_dict, context)


def add_account (request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		form = forms.CustomerForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			# print("Acct added: {} -- {}".format(form.acct, form.name))

			return accounts(request)
		else:
			print form.errors
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	return render_to_response('tracker/add_account.html', context_dict, context)


def remove_account (request, account_name_url):
	"""	Method to 'remove' an account (really just deactivating it)
	This isn't right--I copied from the add_account, but I'm not sure
	it'll actually need a form... """
	context = RequestContext(request)

	# account_name = decode_url(account_name_url)
	account_name = account_name_url.replace(' ', '_')
	context_dict = {'account_name': account_name,
					'account_name_url': account_name_url}

	if request.method == 'GET':
		_customer = Customer.objects.get(name = account_name)
		_customer.closedate = date.today()
		_customer.status = 0
		_customer.save()
		context_dict['message'] = "Account {} deactivated successfully.".format(_customer.acct)

		return accounts(request, context_dict, context)

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
