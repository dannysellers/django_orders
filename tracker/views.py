# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import date
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Customer, Inventory
# import forms


def index (request):
	context = RequestContext(request)
	context_dict = {}

	context_dict['cust_count'] = Customer.objects.count()
	context_dict['cust_act_count'] = Customer.objects.filter(status__exact = 1).count()
	context_dict['item_count'] = Inventory.objects.count()

	storage_fee_count = 0
	for item in Inventory.objects.all():
		if abs((item.arrival - date.today()).days) > 7:
			storage_fee_count += 1
	context_dict['item_storage_count'] = storage_fee_count

	return render_to_response('tracker/index.html', context_dict, context)


def about (request):
	context = RequestContext(request)
	context_dict = {'name': 'About'}

	return render_to_response('tracker/about.html', context_dict, context)