from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
# from django.core.urlresolvers import reverse

from datetime import date
import utils
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

	""" Capture /accounts?remove=<acct> """
	if remove:
		try:
			_inv = Inventory.objects.filter(owner=remove).exclude(status=4)
			if not _inv:  # If the customer has no items currently in storage, deactivate
				remove_account(account_num=remove)
			else:
				# TODO: Seek confirmation if the customer has inventory
				pass  # this customer still has inventory in storage
		except Customer.DoesNotExist:
			context_dict['error_message'] = "Account {} not found. No changes made.".format(remove)
		finally:
			# TODO: This message isn't being passed / displayed properly
			context_dict['message'] = "Account {} deactivated successfully.".format(remove)
			return HttpResponseRedirect('/accounts?accts=active', context_dict)

	else:
		header_list = ['Account', 'Name', 'Create Date']
		if accts:
			try:
				# Parse accts argument, retrieve list of customers
				if accts == "active":
					customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)
					context_dict['head_text'] = 'Active '

				elif accts == "all":
					customer_list = Customer.objects.all()
					context_dict['status_column'] = True  # flag
					header_list.insert(2, 'Status')
					header_list += ['Close Date']
					context_dict['head_text'] = 'All '

				elif accts == "inactive":
					customer_list = Customer.objects.order_by('acct').filter(status__exact = 0)
					header_list += ['Close Date']
					context_dict['head_text'] = 'Inactive '

				else:
					customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)
					context_dict['head_text'] = 'Active '

				context_dict['head_text'] += 'accounts'
				context_dict['num_accts'] = len(customer_list)

			except Customer.DoesNotExist:
				context_dict['error_message'] = "No accounts found."
				customer_list = []
			""" If no arguments, return all active accounts """
		else:
			try:
				customer_list = Customer.objects.order_by('acct').filter(status__iexact = 1)

			except Customer.DoesNotExist:
				context_dict['error_message'] = "No accounts found."
				customer_list = []

		# Prepare data for template
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

	return render_to_response('tracker/accounts.html', context_dict, context)


def account_page (request, account_url):
	# acct = request.GET.get('acct')
	# if not account_url:
	# 	account_url = acct
	context = RequestContext(request)
	context_dict = {}

	header_list = ['Account', 'Name', 'Email', 'Status', 'Create Date']
	context_dict['headers'] = header_list

	# Get account
	account_acct = account_url
	context_dict['account_url'] = account_url
	try:
		customer = Customer.objects.get(acct = account_acct)
		# Show only items still in inventory
		cust_items = Inventory.objects.order_by('itemid').filter(owner = customer).exclude(status=4)
		if cust_items:
			context_dict['inventory_list'] = cust_items
			context_dict['count'] = len(cust_items)
			context_dict['storage_fees'] = utils.calc_storage_fees(customer.acct)
		else:
			context_dict['inv_message'] = "This customer has no items stored in inventory."
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
	context_dict['inv_headers'] = ['ID', '# of Cartons', 'Volume', 'Storage Fees', 'Status', 'Arrival']

	return render_to_response('tracker/accounts.html', context_dict, context)


def add_account (request):
	context = RequestContext(request)
	context_dict = {}

	context_dict['head_text'] = 'Add Account'
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
	print("Account to remove: {}".format(account_num))

	try:
		_customer = Customer.objects.get(acct = account_num)

		_customer.closedate = date.today()
		_customer.status = 0
		_customer.save()
		# context_dict['message'] = "Account {} deactivated successfully.".format(_customer.acct)

		# return HttpResponseRedirect('/accounts?accts=active')
		return dict(message="Account {} deactivated successfully.".format(_customer.acct))
	except Customer.DoesNotExist:
		return dict(message="Account {} not found. No changes made.".format(account_num))