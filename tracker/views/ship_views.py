from ..models import *
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_control
from django.core.urlresolvers import reverse
import re


# Disable caching by browser
@cache_control(no_cache = True)
@login_required
def shipment (request, shipid):
    """
    Overview page for an individual shipment
    """
    context = RequestContext(request)
    context_dict = {}

    try:
        _shipment = Shipment.objects.get(shipid = shipid)
    except Shipment.DoesNotExist:
        messages.add_message(request, messages.ERROR, "No shipment found with ID {}!".format(shipid))
        return HttpResponseRedirect('/inventory?status=stored')

    context_dict['shipment'] = _shipment

    # Overview table
    header_list = ['Owner', 'Owner Acct', 'Palletized', 'Arrival', 'Departure',
                   'Work Order', 'Status', 'Tracking #']
    if int(_shipment.status) != 4:
        header_list.remove('Departure')
    else:
        header_list.remove('Arrival')

    context_dict['headers'] = header_list

    # Itemlist table
    context_dict['item_headers'] = ['Item ID', 'Volume', 'Storage Fees', 'Status']

    # Shipment Operation table
    context_dict['shipop_headers'] = ['Op ID', 'Time', 'Status', 'User']

    # Extras table
    context_dict['extras_headers'] = ['Quantity', 'Unit Cost', 'Total Cost', 'Description']

    return render_to_response('tracker/shipment.html', context_dict, context)


@login_required
def ship_info (request):
    """
    Function to handle receiving shipment info from form id="ship_info"
    """
    if request.method != 'POST':
        messages.add_message(request, messages.ERROR,
                             "Improper request. Try submitting a form from a shipment page.")
        return HttpResponseRedirect('/')
    else:
        # TODO: Prohibit changing status to current status / duplicate ShipOp items (same for items)
        # Shipment information
        shipid = request.GET['shipid']
        try:
            _shipment = Shipment.objects.get(shipid = shipid)
            _shipment.labor_time = request.POST['labor_time']
            _shipment.notes = request.POST['notes']
            if 'palletized' not in request.POST:
                # When the box is not checked, it's not passed at all :\
                _shipment.palletized = False
            else:
                _shipment.palletized = True
            _shipment.tracking_number = request.POST['tracking_number']

            itemcount = 0
            itemlist = []
            for key, value in request.POST.iteritems():
                if '_' in key:
                    num_item = key.split('_')[1]
                    # Get only the checkboxes with name 'item_#'
                    n = re.match(r'^\d+$', num_item)
                    if n:
                        itemcount += 1
                        _item = _shipment.inventory.get(itemid = num_item)
                        itemlist.append(_item)

            _status = request.POST['item_status']

            # If all items' statuses changed, change the shipment status too
            if itemcount == _shipment.inventory.count():
                _shipment.set_status(_status)

            _shipment.save()

        except Shipment.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Shipment {} not found!".format(shipid))
            return HttpResponseRedirect('/shipment/{}'.format(shipid))

        messages.add_message(request, messages.SUCCESS, "Shipment {} information updated.".format(shipid))
        return HttpResponseRedirect('/shipment/{}'.format(shipid))


@login_required
def add_shipment (request, account, order=0):
    """
    Function to create a new Shipment and associate it with 'account'.

    If 'order' == 0, a Work Order has not yet been received (and must be
    linked later). If 'order' != 0, 'order' is the ID of stored WorkOrder.
    """
    context = RequestContext(request)
    context_dict = {}

    try:
        customer = Customer.objects.get(acct = account)
        context_dict['customer'] = customer
    except Customer.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Customer {} not found.".format(account))
        return render_to_response('tracker/add_customer.html',
                                  context_dict,
                                  context)

    if order != '0':
        try:
            _order = WorkOrder.objects.get(id = order)
            context_dict['order_list'] = [_order]
        except WorkOrder.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Order \
            {} not found. Link the shipment to an Order \
            <a href='/workorders/incomplete/'>here</a>.".format(order))
            return HttpResponseRedirect(reverse('account_detail', kwargs = {'account_id': customer.acct}))
    else:
        order_list = WorkOrder.objects.filter(owner = customer) \
            .exclude(status = 999).exclude(shipment__isnull = False)
        context_dict['order_list'] = order_list

    if request.method == 'POST':
        labor_time = request.POST.get('labor_time', '00')
        notes = request.POST.get('notes', 'No notes yet.')
        tracking_number = request.POST.get('tracking_number', '00000')
        palletized = request.POST.get('palletized', False)
        if palletized == 'on':
            palletized = True

        linked_order = request.POST.get('order')
        if linked_order != 'Order not yet received':
            linked_order_id = re.findall('#(\d+):', linked_order)[0]
            order = WorkOrder.objects.get(id = linked_order_id)
        else:
            order = None

        _shipment = Shipment.objects.create_shipment(owner = customer, palletized = palletized,
                                                     labor_time = labor_time, notes = notes,
                                                     tracking_number = tracking_number)

        # If there is an order, link it and the shipment
        if order:
            order.shipment = _shipment
            order.save()

        # Dimensions are return as ordered lists of length, width, height, quantity
        quantity_set = request.POST.getlist('quantity')
        length_set = request.POST.getlist('length')
        width_set = request.POST.getlist('width')
        height_set = request.POST.getlist('height')
        for index, quantity in enumerate(quantity_set):
            for carton in range(int(quantity)):
                index = int(index)
                _length = length_set[index]
                _width = width_set[index]
                _height = height_set[index]
                Inventory.objects.create_inventory(shipset = _shipment,
                                                   length = _length,
                                                   width = _width,
                                                   height = _height)

        messages.add_message(request, messages.SUCCESS, "Shipment {}, \
        containing {} items created successfully.".format(_shipment.shipid, _shipment.inventory.count()))
        return HttpResponseRedirect('/shipment/{}'.format(_shipment.shipid))
    else:
        return render_to_response('tracker/add_shipment_form.html', context_dict, context)


@login_required
def ship_extras (request):
    """
    Function to process incoming shipment optional extra form POSTS, form id='ship_extras'
    """
    shipid = int(request.GET['shipid'])

    try:
        _shipment = Shipment.objects.get(shipid = shipid)
    except Shipment.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Shipment {} not found.".format(shipid))
        return HttpResponseRedirect('/shipment/{}'.format(shipid))

    if request.method == 'POST':
        quantity = float(request.POST['quantity'])
        unit_cost = float(request.POST['unit_cost'])
        description = request.POST['description']
        OptExtras.objects.create_optextra(shipment = _shipment, quantity = quantity,
                                          unit_cost = unit_cost, description = description)
        messages.add_message(request, messages.SUCCESS, "{} {} added successfully.".format(quantity, description))
    else:
        messages.add_message(request, messages.ERROR, "Invalid request received. Try submitting a form.")

    return HttpResponseRedirect('/shipment/{}'.format(shipid))


@login_required
def link_shipment (request, shipid):
    """
    Function to handle linking Shipment and WorkOrder objects
    """
    if request.method != 'POST':
        pass
    else:
        _shipment = Shipment.objects.get(shipid = shipid)

        order_desc = request.POST['orderid']
        order_id = re.findall('#(\d+):', order_desc)[0]
        order = WorkOrder.objects.get(id = order_id)

        order.shipment = _shipment
        order.save()

        messages.add_message(request, messages.SUCCESS, "Shipment {1} and Order {0} linked successfully.".format(
            order.id, shipment.shipid
        ))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))