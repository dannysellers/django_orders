from models import *
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_control
import re


# Disable caching by browser
@cache_control(no_cache = True)
def shipment (request):
	"""
	Overview page for an individual shipment
	"""
	context = RequestContext(request)
	context_dict = {}

	shipid = request.GET['id']
	try:
		_shipment = Shipment.objects.get(shipid = shipid)
	except Shipment.DoesNotExist:
		messages.add_message(request, messages.ERROR, "No shipment found with ID {}!".format(shipid))
		return HttpResponseRedirect('/inventory?status=stored')

	context_dict['shipment'] = _shipment

	# Overview table
	header_list = ['Owner', 'Owner Acct', 'Palletized', 'Arrival', 'Departure',
				   'Labor time', 'Status', 'Tracking #']
	if int(_shipment.status) != 4:
		header_list.remove('Departure')
	else:
		header_list.remove('Arrival')

	context_dict['headers'] = header_list

	# Itemlist table
	context_dict['item_headers'] = ['Item ID', 'Volume', 'Storage Fees', 'Status']

	# Shipment Operation table
	context_dict['shipop_headers'] = ['Op ID', 'Time', 'Code', 'User']

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
							 "Improper request. Try submitting a form from a shipment view.")
		return HttpResponseRedirect('/')
	else:
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
						_item = _shipment.inventory_set.get(itemid = num_item)
						itemlist.append(_item)

			_status = request.POST['item_status']

			# If all items' statuses changed, change the shipment status too
			if itemcount == _shipment.inventory_set.count():
				for item in itemlist:
					item.status = _status
					item.save({'user': request.user})
				_shipment.status = _status

			_shipment.save({'user': request.user})

		except Shipment.DoesNotExist:
			messages.add_message(request, messages.ERROR, "Shipment {} not found!".format(shipid))
			return HttpResponseRedirect('/shipment?id={}'.format(shipid))

		messages.add_message(request, messages.SUCCESS, "Shipment {} information updated.".format(shipid))
		return HttpResponseRedirect('/shipment?id={}'.format(shipid))


@login_required
def add_shipment (request, account_url):
	context = RequestContext(request)
	context_dict = {}

	try:
		customer = Customer.objects.get(acct = account_url)
		context_dict['customer'] = customer
	except Customer.DoesNotExist:
		messages.add_message(request, messages.ERROR, "Customer {} not found.".format(account_url))
		return render_to_response('tracker/add_customer.html',
								  context_dict,
								  context)

	if request.method == 'POST':
		labor_time = request.POST.get('labor_time', '00')
		notes = request.POST.get('notes', 'No notes yet.')
		tracking_number = request.POST.get('tracking_number', '00000')
		palletized = request.POST.get('palletized', False)
		if palletized == 'on':
			palletized = True

		_shipment = Shipment.objects.create_shipment(owner = customer, palletized = palletized,
													 labor_time = labor_time, notes = notes,
													 tracking_number = tracking_number)

		# Dimensions are return as ordered lists of length, width, height, quantity
		quantity_set = request.POST.getlist('quantity')
		height_set = request.POST.getlist('height')
		width_set = request.POST.getlist('width')
		length_set = request.POST.getlist('length')
		for i in range(len(quantity_set)):
			Inventory.objects.create_inventory(shipset = _shipment, length = length_set[i],
											   width = width_set[i], height = height_set[i])

		messages.add_message(request, messages.SUCCESS,
							 "Shipment {} of {} items created successfully.".format(_shipment.shipid,
																					_shipment.inventory_set.count()))
		return HttpResponseRedirect('/shipments?id={}'.format(_shipment.shipid))
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
		return HttpResponseRedirect('/shipment?id={}'.format(shipid))

	if request.method == 'POST':
		quantity = float(request.POST['quantity'])
		unit_cost = float(request.POST['unit_cost'])
		description = request.POST['description']
		OptExtras.objects.create_optextra(shipment = _shipment, quantity = quantity,
										  unit_cost = unit_cost, description = description)
		messages.add_message(request, messages.SUCCESS, "{} {} added successfully.".format(quantity, description))
	else:
		messages.add_message(request, messages.ERROR, "Invalid request received. Try submitting a form.")

	return HttpResponseRedirect('/shipment?id={}'.format(shipid))