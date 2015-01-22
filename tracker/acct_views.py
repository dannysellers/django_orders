from datetime import date

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control
import utils
from models import Customer, Inventory
import forms


def encode_url (url):
	return url.replace(' ', '_')


def decode_url (url):
	return url.replace('_', ' ')


@cache_control(no_cache = True)
def accounts (request):
	context = RequestContext(request)
	context_dict = dict()

	# URL params
	acct = request.GET.get('acct')
	accts = request.GET.get('accts')
	remove = request.GET.get('remove')
	confirm_remove = request.GET.get('confirm_remove')

	if acct:
		# Handles /accounts?acct={}
		return redirect('/accounts/{}/'.format(acct))

	""" Capture /accounts?remove=<acct> """
	if remove:
		if request.user.is_authenticated:
			if confirm_remove:
				messages.add_message(request, messages.WARNING,
									 "Confirmation of deactivation")
				if remove_account(account_num = remove):
					messages.add_message(request, messages.SUCCESS,
										 "Account {} deactivated successfully".format(remove))
					return HttpResponseRedirect('/accounts?accts=active', context_dict)

			else:
				try:
					# If the customer has no items currently in storage, deactivate
					if not Inventory.objects.filter(owner = remove).exclude(status = 4):
						# remove_account() returns False on Customer.DoesNotExist
						if not remove_account(account_num = remove):
							messages.add_message(request, messages.WARNING,
												 "Account {} not found. No changes made.".format(remove))
							return redirect('/accounts?accts=active', context_dict)
						else:
							messages.add_message(request, messages.SUCCESS,
												 "Account {} deactivated successfully".format(remove))
							return redirect('/accounts?accts=active', context_dict)
					else:
						# TODO: Do confirmation for removing customers with stored items
						messages.add_message(request, messages.WARNING,
											 "This customer has items in inventory. Proceed with deactivation?")
						context_dict['confirm_remove'] = 'Confirm'
						return render_to_response('/accounts?remove={}&confirm_remove=False'.format(remove),
												  context_dict)

				except Customer.DoesNotExist:
					messages.add_message(request, messages.ERROR,
										 "Account {} not found. No changes made.".format(remove))
					return HttpResponseRedirect('/accounts?accts=active', context_dict)
		else:
			messages.add_message(request, messages.ERROR, "You are not logged in.")
			return HttpResponseRedirect('/accounts?accts=active', context_dict)

	else:
		header_list = ['Account', 'Name', 'Create Date', 'Stored Shipments', 'Storage Fees']
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
					header_list.insert(-2, 'Close Date')
					context_dict['head_text'] = 'All '

				elif accts == "inactive":
					customer_list = Customer.objects.order_by('acct').filter(status__exact = 0)
					header_list.remove('Stored Shipments')
					header_list.insert(-1, 'Close Date')
					context_dict['head_text'] = 'Inactive '

				else:
					customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)
					context_dict['head_text'] = 'Active '

				context_dict['head_text'] += 'accounts'

			except Customer.DoesNotExist:
				messages.add_message(request, messages.WARNING, "No accounts found.")
				customer_list = []
			""" If no arguments, return all active accounts """
		else:
			try:
				customer_list = Customer.objects.order_by('acct').filter(status__iexact = 1)
				context_dict['head_text'] = 'Active'

			except Customer.DoesNotExist:
				messages.add_message(request, messages.WARNING, "No accounts found.")
				customer_list = []

		# Prepare data for template
		context_dict['headers'] = header_list
		context_dict['num_accts'] = len(customer_list)

		context_dict['customer_list'] = customer_list

	return render_to_response('tracker/accounts.html', context_dict, context)


def account_page (request, account_url):
	context = RequestContext(request)
	context_dict = dict()

	header_list = ['Name', 'Account', 'Email', 'Status', 'Create Date']
	context_dict['headers'] = header_list

	# Get account
	context_dict['account_url'] = account_url
	try:
		customer = Customer.objects.get(acct = account_url)
		# Show only items still in inventory
		if customer.inventory_set.exclude(status = 4).count():
			cust_shipments = customer.shipment_set.all().exclude(status = 4)
			context_dict['shipment_list'] = cust_shipments
			context_dict['storage_fees'] = utils.calc_storage_fees(customer.acct)
		else:
			messages.add_message(request, messages.INFO, "This customer has no items stored in inventory.")
	except Customer.DoesNotExist:
		messages.add_message(request, messages.ERROR, "Account {} not found.".format(account_url))
		return render_to_response('tracker/accounts.html', context_dict, context)

	context_dict['customer'] = customer

	# Table cells
	if str(customer.status) == '0':
		context_dict['account_status'] = 'Inactive'
		context_dict['headers'].append('Close Date')
		context_dict['close_date'] = str(customer.closedate)
	elif str(customer.status) == '1':
		context_dict['account_status'] = 'Active'
	else:
		context_dict['account_status'] = str(customer.status)

	# Inventory table
	context_dict['inv_headers'] = ['Ship ID', 'Item ID', 'Volume', 'Storage Fees', 'Status', 'Arrival']

	return render_to_response('tracker/accounts.html', context_dict, context)


@login_required
@cache_control(no_cache = True)
def acct_info (request):
	acct = request.GET.get('acct')
	if request.method != 'POST':
		messages.add_message(request, messages.ERROR, "Improper request type. Try submitting a form instead.")
		return HttpResponseRedirect('/accounts?acct={}'.format(acct))
	else:
		try:
			customer = Customer.objects.get(acct = acct)
		except Customer.DoesNotExist:
			messages.add_message(request, messages.ERROR, "Could not find customer with acct #{}".format(acct))
			return HttpResponseRedirect('/accounts?accts=active')
		else:
			customer.notes = request.POST['notes']
			customer.email = request.POST['email']
			customer.name = request.POST['name']
			customer.notes = request.POST['notes']
			customer.acct = request.POST['acct']  # TODO: Confirmation on changing acct number
		finally:
			customer.save()
			messages.add_message(request, messages.SUCCESS, "Account information updated successfully.")
			return HttpResponseRedirect('/accounts/{}'.format(customer.acct))


@login_required
def add_account (request):
	context = RequestContext(request)
	context_dict = dict()

	context_dict['head_text'] = 'Add Account'
	if request.method == 'POST':
		form = forms.CustomerForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts?accts=active')
		else:
			print form.errors
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	context_dict['customer'] = '_'  # template flag
	return render_to_response('tracker/form.html', context_dict, context)


@login_required
def remove_account (account_num):
	print("remove_account(): {}".format(account_num))

	try:
		_customer = Customer.objects.get(acct = account_num)

		_customer.closedate = date.today()
		_customer.status = 0
		_customer.save()

		return True
	except Customer.DoesNotExist:
		return False