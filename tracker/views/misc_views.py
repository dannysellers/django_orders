from datetime import date, timedelta

from django.db.models import Sum
from django.template import RequestContext
from django.shortcuts import render_to_response
from ..models import Shipment, Inventory, Customer, WorkOrder


def index (request):
    context = RequestContext(request)
    context_dict = dict()

    if not request.user.is_authenticated():
        return render_to_response('tracker/login.html', context_dict, context)
    else:
        context_dict['cust_act_count'] = Customer.objects.filter(status = 1).count()
        context_dict['item_count'] = Inventory.objects.exclude(status = 4).count()
        context_dict['ship_count'] = Shipment.objects.exclude(status = 4).count()
        context_dict['total_item_volume'] = Inventory.objects.exclude(status = 4).aggregate(
            Sum('volume'))['volume__sum']
        context_dict['work_order_count'] = WorkOrder.objects.exclude(status = 4).exclude(
            status = 999).count()
        context_dict['unmatched_orders'] = WorkOrder.objects.exclude(status = 4).exclude(
            status = 999).exclude(shipment__isnull = False).count()

        ten_days_ago = date.today() - timedelta(days = 10)

        context_dict['item_storage_count'] = Inventory.objects.exclude(status = 4) \
            .filter(arrival__lte = ten_days_ago).count()
        context_dict['item_no_storage_count'] = Inventory.objects.exclude(status = 4) \
            .filter(arrival__range = (ten_days_ago, date.today())).count()

        return render_to_response('tracker/index.html', context_dict, context)
