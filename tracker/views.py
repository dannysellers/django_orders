# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
# from datetime import date
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Customer, Inventory
# import forms


def index (request):
	context = RequestContext(request)
	context_dict = {}

	context_dict['cust_count'] = len(Customer.objects.all())
	context_dict['cust_act_count'] = len(Customer.objects.all().filter(status__exact = 1))
	context_dict['item_count'] = len(Inventory.objects.all())

	return render_to_response('tracker/index.html', context_dict, context)


def about (request):
	context = RequestContext(request)
	context_dict = {'name': 'About'}

	return render_to_response('tracker/about.html', context_dict, context)