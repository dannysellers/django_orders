from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json
from ..models import WorkOrder, Shipment


@login_required
def work_orders (request):
    context = RequestContext(request)
    context_dict = dict()

    completed_orders = WorkOrder.objects.all().exclude(status = 4)

    context_dict['orders'] = completed_orders
    context_dict['count'] = completed_orders.count()

    context_dict['headers'] = ['Order ID', 'Ship ID', 'Owner', 'Create Date', 'Status']

    return render_to_response('tracker/workorder_list.html', context_dict, context)


@login_required
def work_order_detail (request, id):
    context = RequestContext(request)
    context_dict = dict()

    context_dict['order'] = WorkOrder.objects.get(id = id)
    context_dict['orderop_headers'] = ['Op ID', 'Time', 'Status', 'User']

    return render_to_response('tracker/workorder_detail.html', context_dict, context)


@login_required
def submit_work_order (request):
    # TODO: Will work orders ever be created/submitted not by the API?
    # context = RequestContext(request)
    # context_dict = ()

    return HttpResponse("This is the method to create a work order", content_type = 'application/json')


@csrf_exempt
def get_unmatched_shipments (request, order_id):
    """
    AJAX function to list shipments that have no associated Work Order.

    Returns shipments belonging to a particular Customer (order owner)
    that are unmatched and still in storage (redundant?)
    """
    context_dict = dict()

    order = WorkOrder.objects.get(id = order_id)
    _owner = order.owner

    _list = Shipment.objects.exclude(status = 4)\
        .filter(owner = _owner)\
        .exclude(workorder__isnull = False)
    context_dict['list'] = [str(shipment) for shipment in _list]

    return HttpResponse(json.dumps(context_dict), content_type = 'application/json')