from datetime import date, timedelta

from django.db.models import Sum
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import Shipment, Inventory, Customer, WorkOrder


def index (request):
    context = RequestContext(request)
    context_dict = dict()

    if request.user.is_anonymous():
        return render_to_response('tracker/login.html', context_dict, context)
    else:
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


@login_required
def work_orders (request):
    context = RequestContext(request)
    context_dict = dict()

    completed_orders = WorkOrder.objects.all().exclude(status = 4)

    context_dict['orders'] = completed_orders
    context_dict['count'] = completed_orders.count()

    context_dict['headers'] = ['Order ID', 'Ship ID', 'Owner', 'Create Date', 'Status']

    return render_to_response('tracker/workorders.html', context_dict, context)


@login_required
def work_order_detail(request, id):
    context = RequestContext(request)
    context_dict = dict()

    context_dict['order'] = WorkOrder.objects.get(id = id)
    context_dict['headers'] = ['Owner', 'Owner Acct', 'Create Date', 'Quantity', 'Status']
    context_dict['orderop_headers'] = ['Op ID', 'Time', 'Status', 'User']

    return render_to_response('tracker/workorder_detail.html', context_dict, context)


@login_required
def submit_work_order (request):
    # TODO: Will work orders ever be created/submitted not by the API?
    # context = RequestContext(request)
    # context_dict = ()

    return HttpResponse("This is the method to create a work order", content_type = 'application/json')