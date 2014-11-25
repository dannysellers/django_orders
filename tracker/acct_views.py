from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
# from django.core.urlresolvers import reverse

from datetime import date

from models import Customer, Inventory
import forms


def encode_url (url):
	return url.replace(' ', '_')


def decode_url (url):
	return url.replace('_', ' ')


def accounts (request):
	context = RequestContext(request)
	context_dict = {}
	accts = request.GET.get('accts')
	remove = request.GET.get('remove')

	# Capture /accounts?remove=<acct>
	if remove:
		try:
			remove_account(account_num=remove)
		except Customer.DoesNotExist:
			context_dict['error_message'] = "Account {} not found. No changes made.".format(remove)
		finally:
			context_dict['message'] = "Account {} deactivated successfully.".format(remove)

	try:
		header_list = ['Account', 'Name', 'Status']

		# Parse accts argument, retrieve list of customers
		if accts == "active":
			customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)[:10]
		elif accts == "all":
			customer_list = Customer.objects.all()[:10]
			header_list += ['Close Date']
		elif accts == "inactive":
			customer_list = Customer.objects.order_by('acct').filter(status__exact = 0)
			header_list += ['Close Date']
		else:
			customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)[:10]

		context_dict['headers'] = header_list

		# Replace spaces with underscores to retrieve URL
		for customer in customer_list:
			customer.url = 'accounts/' + str(customer.acct)
			# Replace 0 and 1 with account status
			# This seems to show Active or Inactive for all people in the list
			if str(customer.status) == '0':
				context_dict['account_status'] = 'Inactive'
			elif str(customer.status) == '1':
				context_dict['account_status'] = 'Active'
			else:
				context_dict['account_status'] = str(customer.status)
			
			# TODO: How to use enumerated choices?

		context_dict['customer_list'] = customer_list

	except Customer.DoesNotExist:
		context_dict['error_message'] = "No accounts found."

	return render_to_response('tracker/accounts.html', context_dict, context)


def account_page (request, account_url):
	context = RequestContext(request)
	context_dict = {}
	header_list = ['Account', 'Name', 'Email', 'Status']
	context_dict['headers'] = header_list

	account_acct = account_url
	context_dict['account_url'] = account_url
	try:
		customer = Customer.objects.get(acct = account_acct)
	except Customer.DoesNotExist:
		context_dict['error_message'] = "Account {} not found.".format(
			account_acct)
		return render_to_response('tracker/accounts.html', context_dict, context)

	context_dict['customer'] = customer

	# Table cells
	if str(customer.status) == '0':
		context_dict['account_status'] = 'Inactive'
		context_dict['headers'].append('Date Closed')
		context_dict['close_date'] = str(customer.closedate)
	elif str(customer.status) == '1':
		context_dict['account_status'] = 'Active'
	else:
		context_dict['account_status'] = str(customer.status)

	# Inventory table
	context_dict['inv_headers'] = ['ID', 'Quantity', 'Weight', 'Storage Fees', 'Status']
	cust_items = Inventory.objects.order_by('itemid').filter(owner = customer)
	if cust_items:
		context_dict['inventory_list'] = cust_items

	return render_to_response('tracker/accounts.html', context_dict, context)


def add_account (request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		form = forms.CustomerForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			# print("Acct added: {} -- {}".format(form.acct, form.name))

			return redirect(accounts, permanent=True)
		else:
			print form.errors
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	return render_to_response('tracker/add_account.html', context_dict, context)


def remove_account (account_num):
	"""
	Method to remove (deactivate) an account. There's no form or page here,
	so I'm thinking it might make more sense as just a (AJAX?) request?
	"""
	print("Account to remove: {}".format(account_num))

	try:
		_customer = Customer.objects.get(acct = account_num)
		account_name = _customer.name

		context_dict = {'account_name': account_name,
						'account_num': account_num}

		_customer.closedate = date.today()
		_customer.status = 0
		_customer.save()
		# context_dict['message'] = "Account {} deactivated successfully.".format(_customer.acct)

		return HttpResponseRedirect('/accounts?accts=active', context_dict)
	except Customer.DoesNotExist:
		# TODO: Fix error return message
		return dict(message="Account {} not found. No changes made.".format(account_num))