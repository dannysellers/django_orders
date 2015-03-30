from datetime import date

from django.db.models import Sum
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from ..models import *


def index (request):
    context = RequestContext(request)
    context_dict = dict()

    context_dict['cust_act_count'] = Customer.objects.filter(status = 1).count()
    context_dict['item_count'] = Inventory.objects.exclude(status = 4).count()
    context_dict['ship_count'] = Shipment.objects.exclude(status = 4).count()
    context_dict['total_item_volume'] = Inventory.objects.exclude(status = 4).aggregate(Sum('volume'))['volume__sum']

    ten_days_ago = date.today() - timedelta(days = 10)

    context_dict['item_storage_count'] = Inventory.objects.exclude(status = 4) \
        .filter(arrival__lte = ten_days_ago).count()
    context_dict['item_no_storage_count'] = Inventory.objects.exclude(status = 4) \
        .filter(arrival__range = (ten_days_ago, date.today())).count()

    return render_to_response('tracker/index.html', context_dict, context)


def work_orders (request):
    # context = RequestContext(request)
    # context_dict = dict()

    orders = WorkOrder.objects.all()

    return HttpResponse("There are {} work orders on file".format(len(orders)), content_type = 'application/json')


def submit_work_order (request):
    # context = RequestContext(request)
    # context_dict = ()

    return HttpResponse("This is the method to create a work order", content_type='application/json')