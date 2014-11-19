from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Customer
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
	context_dict = {'name': 'Accounts'}

	return render_to_response('tracker/accounts.html', context_dict, context)


def accountpage (request, account_name_url):
	context = RequestContext(request)

	# Change underscores in the account name to spaces
	# The URL will have an underscore, which replaced with a space corresponds to the customer
	account_name = decode_url(account_name_url)
	context_dict = {'account_name': account_name,
					'account_name_url': account_name_url}

	try:
		_customer = Customer.objects.get(name__iexact = account_name)
		context_dict['customer'] = _customer

		context_dict['account_acct'] = _customer.acct
		context_dict['account_email'] = _customer.email

	except Customer.DoesNotExist:
		# If no customer's found, pass nothing
		pass

	return render_to_response('tracker/accounts.html', context_dict, context)


def add_account (request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		form = forms.CustomerForm(request.POST)

		if form.is_valid():
			form.save(commit = True)

			return index(request)
		else:
			print form.errors
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	return render_to_response('tracker/add_account.html', context_dict, context)


def add_item (request, account_name_url):
	print account_name_url
	return HttpResponse("This page is for adding items to a customer's inventory.")


def inventory (request):
	context = RequestContext(request)
	context_dict = {'name': 'Inventory'}

	return render_to_response('tracker/inventory.html', context_dict, context)