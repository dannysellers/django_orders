# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Customer
import forms


def encode_url (url):
	return url.replace(' ', '_')


def decode_url (url):
	return url.replace('_', ' ')


def accounts (request, bool_active='active'):
	context = RequestContext(request)
	context_dict = {}

	try:
		if bool_active == "active":
			customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)[:5]
		elif bool_active == "all":
			customer_list = Customer.objects.all()[:5]
		else:
			customer_list = Customer.objects.order_by('acct').filter(status__exact = 1)[:5]
		# paginator = Paginator(customer_list, 15)  # show 15 customers per page

		# page = request.GET.get('page')

		header_list = ['Account', 'Name', 'Business Name', 'Status']
		context_dict['headers'] = header_list

		# Replace spaces with underscores to retrieve URL
		for customer in customer_list:
			customer.url = encode_url(customer.name)
			# TODO: How to use enumerated choices?
			# if customer.status == 0:
			# 	customer.status = 'Inactive'
			# else:
			# 	customer.status = 'Active'

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


def account_page (request, account_url):
	# TODO: Handle customers with multiple accounts
	context = RequestContext(request)
	context_dict = {'Headers': ['Account', 'Name', 'Business Name', 'Email']}

	# Change underscores in the account name to spaces
	# The URL will have an underscore, which replaced
	# with a space corresponds to the customer
	if isinstance(account_url, str):
		account_name = decode_url(account_url)
		context_dict['account_name'] = account_name
		context_dict['account_url'] = account_url
		try:
			_customer = Customer.objects.get(name__iexact = account_name)
		except Customer.DoesNotExist:
			context_dict['error_message'] = "Sorry, I couldn't find {}'s account.".format(
				account_name)
	elif isinstance(account_url, int):
		account_acct = account_url
		context_dict['account_name'] = account_url
		context_dict['account_url'] = account_url
		try:
			_customer = Customer.objects.get(acct__exact = account_acct)
		except Customer.DoesNotExist:
			context_dict['error_message'] = "Sorry, I couldn't find account {}.".format(
				account_acct)

	# _customer = Customer.objects.get(name__iexact = account_name)
	context_dict['customer'] = _customer

	context_dict['account_name'] = _customer.name
	context_dict['account_acct'] = _customer.acct
	context_dict['account_email'] = _customer.email

	return render_to_response('tracker/accounts.html', context_dict, context)


def add_account (request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		form = forms.CustomerForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			# print("Acct added: {} -- {}".format(form.acct, form.name))

			# TODO: Return to populated account page, rather than blank
			return render_to_response('tracker/accounts.html', context)
			# return accounts(context)
		else:
			print form.errors
	else:
		form = forms.CustomerForm()

	context_dict['form'] = form
	return render_to_response('tracker/add_account.html', context_dict, context)


def remove_account (request, account_num_url):
	context = RequestContext(request)

	_customer = Customer.objects.get(acct = account_num_url)
	account_name = _customer.name
	# account_name = decode_url(account_num_url)
	# account_name = account_name_url.replace(' ', '_')
	context_dict = {'account_name': account_name,
					'account_num_url': account_num_url}

	if request.method == 'GET':
		# _customer = Customer.objects.get(name = account_name)
		_customer.closedate = date.today()
		_customer.status = 0
		_customer.save()
		context_dict['message'] = "Account {} deactivated successfully.".format(_customer.acct)
		return accounts(context)

	return render_to_response('tracker/accounts.html', context)