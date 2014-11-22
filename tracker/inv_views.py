from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Inventory
import forms


def inventory(request):
	context = RequestContext(request)
	context_dict = {}
	context_dict['name'] = 'All Inventory'

	inventory_list = Inventory.objects.all().filter(status=1)
	if inventory_list:
		context_dict['inventory_list'] = inventory_list
	else:
		context_dict['error_message'] = "No items found."

	return render_to_response('tracker/inventory.html', context_dict, context)


def add_item (request, account_name_url):
	print account_name_url
	return HttpResponse("This page is for adding items to a customer's inventory.")