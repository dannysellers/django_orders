from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
	context = RequestContext(request)
	context_dict = {}

	return render_to_response('tracker/index.html', context_dict, context)


def about(request):
	context = RequestContext(request)
	context_dict = {'name': 'About'}

	return render_to_response('tracker/about.html', context_dict, context)


def accounts(request):
	context = RequestContext(request)
	context_dict = {'name': 'Accounts'}

	return render_to_response('tracker/accounts.html', context_dict, context)


def accountpage(request, account_name_url):
	print account_name_url
	return HttpResponse('This page is for individual accounts.')


def add_item(request, account_name_url):
	print account_name_url
	return HttpResponse("This page is for adding items to a customer's inventory.")


def inventory(request):
	context = RequestContext(request)
	context_dict = {'name': 'Inventory'}

	return render_to_response('tracker/inventory.html', context_dict, context)