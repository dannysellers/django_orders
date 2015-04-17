from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import json
from ..models import WorkOrder, Shipment


@login_required
def work_orders (request):
    context = RequestContext(request)
    context_dict = dict()

    wo_filter = request.GET.get('status')

    open_orders = WorkOrder.objects.exclude(status = 4).exclude(status = 999)
    finished_orders = WorkOrder.objects.filter(status = 4)

    header_list = ['Order ID', 'Shipment', 'Owner', 'Create Date', 'Status', '']

    if wo_filter == 'incomplete' or not wo_filter:
        context_dict['orders'] = open_orders
        context_dict['count'] = open_orders.count()
    elif wo_filter == 'complete':
        context_dict['orders'] = finished_orders
        header_list.pop()  # Remove the blank column header over the Delete buttons
        header_list.insert(3, 'Finish Date')
        context_dict['count'] = finished_orders.count()
    else:
        context_dict['orders'] = open_orders
        context_dict['count'] = open_orders.count()

    context_dict['headers'] = header_list

    return render_to_response('tracker/workorder_list.html', context_dict, context)


@login_required
def work_order_detail (request, id):
    context = RequestContext(request)
    context_dict = dict()

    order = WorkOrder.objects.get(id = id)

    header_list = ['Owner', 'Acct', 'Create Date', 'Quantity', 'Status']
    if order.status == 4:
        header_list.index('Complete Date', 3)
    context_dict['headers'] = header_list

    context_dict['order'] = order
    context_dict['orderop_headers'] = ['Op ID', 'Time', 'Status', 'User']

    return render_to_response('tracker/workorder_detail.html', context_dict, context)


@login_required
def remove_work_order (request, id):
    try:
        order = WorkOrder.objects.get(id = id)
        order.remove_order()
        messages.add_message(request, messages.SUCCESS, "Order {} removed.".format(order.id))
    except WorkOrder.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Can't find any Work Order with ID {}".format(id))

    return HttpResponseRedirect('/workorders/')


@login_required
def submit_work_order (request):
    # TODO: Will work orders ever be created/submitted not by the API?
    # context = RequestContext(request)
    # context_dict = ()

    return HttpResponse("This is the method to create a work order", content_type = 'application/json')


@csrf_exempt
def get_unmatched_shipments (request, order_id):
    """
    AJAX function to list Shipments that have no associated Work Order.

    Returns shipments belonging to a particular Customer (order owner)
    that are unmatched and still in storage (redundant?)
    """
    context_dict = dict()

    order = WorkOrder.objects.get(id = order_id)
    _owner = order.owner

    _list = Shipment.objects.exclude(status = 4) \
        .filter(owner = _owner) \
        .exclude(workorder__isnull = False)
    context_dict['list'] = [str(shipment) for shipment in _list]

    return HttpResponse(json.dumps(context_dict), content_type = 'application/json')


@csrf_exempt
def get_unmatched_orders (request, ship_id):
    """
    AJAX function to list Work Orders that have no associated Shipment.

    Returns Work Orders belonging to a particular Customer (shipment owner)
    that are unmatched and not deleted
    """
    context_dict = dict()

    shipment = Shipment.objects.get(shipid = ship_id)
    _owner = shipment.owner

    _list = WorkOrder.objects.exclude(status = 999) \
        .filter(owner = _owner) \
        .exclude(shipment__isnull = False)
    context_dict['list'] = [str(order) for order in _list]

    return HttpResponse(json.dumps(context_dict), content_type = 'application/json')