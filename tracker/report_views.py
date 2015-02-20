try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from datetime import date
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from models import Shipment, Inventory
from templatetags.num_filters import length
from utils import get_shipment_cost


def reports (request):
	return render(request, 'tracker/graphs.html')


@csrf_exempt
def ajax_graph (request):
	"""
	Tallies total number of shipments between specified dates
	:return: CSV
	:rtype: HttpResponse
	"""
	if request.method != 'GET':
		messages.add_message(request, messages.ERROR, "This URL doesn't accept POSTs.")
		return HttpResponseRedirect('')
	else:
		# query_type = query.split("_")

		start_date = request.GET.get('start')
		if not start_date:
			start_date = date(2015, 1, 1)

		finish_date = request.GET.get('finish')
		if not finish_date:
			finish_date = date(2015, 1, 31)

		# TODO: Make this work with dates in different months
		day_labels = range(1, finish_date.day - start_date.day)[::3]

		returned_data = dict(labels = [str(i) for i in day_labels])

		count_dict = {}
		for day in day_labels:
			# TODO: Resolve how to deduce which month/year to use. Maybe just do report by calendar month?
			# labels is a list of days
			# get number of shipments stored per each day in labels
			# tick that up in count_dict
			_date = date(2015, 1, day)
			# model_attr = query_type[0]
			# count_method = query_type[1]

			arrived_shipments = Shipment.objects.filter(arrival__range = (start_date, _date)).count()
			count_dict[day] = arrived_shipments

		data_dict = dict()
		data_dict['label'] = 'Shipments'
		data_dict['fillColor'] = 'rgba(220,220,220,0.5)'
		data_dict['strokeColor'] = 'rgba(220,220,220,0.8)'
		data_dict['pointColor'] = "rgba(220,220,220,1)"
		data_dict['pointStrokeColor'] = "#fff"
		data_dict['pointHighlightFill'] = "#fff"
		data_dict['pointHighlightStroke'] = "rgba(220,220,220,1)"

		data_dict['data'] = count_dict.values()

		returned_data['datasets'] = [data_dict]

		return HttpResponse(json.dumps(returned_data), content_type = 'application/json')


@csrf_exempt
def stored_volume_over_time (request):
	if request.method == 'GET':
		start_date = request.GET.get('start')
		if not start_date:
			start_date = date(2015, 1, 1)

		finish_date = request.GET.get('finish')
		if not finish_date:
			finish_date = date(2015, 1, 31)

		day_labels = range(1, finish_date.day - start_date.day)[::3]
		returned_data = dict(labels = [str(i) for i in day_labels])

		count_dict = {}
		for day in day_labels:
			_date = date(2015, 1, day)
			stored_volume = Inventory.objects. \
				filter(arrival__range = (start_date, _date)). \
				aggregate(Sum('volume'))['volume__sum']
			if not stored_volume:
				stored_volume = 0.00
			count_dict[day] = stored_volume

		data_dict = dict()
		data_dict['label'] = 'Shipments'
		data_dict['fillColor'] = 'rgba(220,220,220,0.5)'
		data_dict['strokeColor'] = 'rgba(220,220,220,0.8)'
		data_dict['pointColor'] = "rgba(220,220,220,1)"
		data_dict['pointStrokeColor'] = "#fff"
		data_dict['pointHighlightFill'] = "#fff"
		data_dict['pointHighlightStroke'] = "rgba(220,220,220,1)"

		data_dict['data'] = count_dict.values()

		returned_data['datasets'] = [data_dict]

		return HttpResponse(json.dumps(returned_data), content_type = 'application/json')


def shipment_report (request, shipid):
	"""
	Create a PDF for the shipment and return as an HTTP Response obj
	:param shipid: ID for the shipment
	:type shipid: int
	:return: Generated PDF
	"""
	# TODO: Change to Weasyprint
	content_type = request.GET.get('type')

	response = HttpResponse(content_type = 'application/pdf')

	shipment = get_object_or_404(Shipment, shipid = shipid)
	owner = str(shipment.owner.name)
	acct = str(shipment.owner.acct)
	items = shipment.inventory_set.all()
	time_generated = str(timezone.now())

	# 'attachment' will prompt the user to download the file. 'inline'
	# will cause most modern browsers to display the PDF within the
	# browser window.
	response['Content-Disposition'] = '{0}; filename="Shipment_{1}_Invoice.pdf"'.format(content_type, shipid)

	temp = StringIO()

	# Page setup
	p = canvas.Canvas(temp)
	page_width = A4[0]
	page_height = A4[1]

	# Margins
	top_margin = page_height - inch
	bottom_margin = 0.75 * inch
	left_margin = 0.75 * inch
	right_margin = page_width - (0.75 * inch)

	# Draw header
	title = 'Shipment {} Invoice'.format(shipid)
	p.setFont('Helvetica', 14)
	p.drawCentredString(page_width / 2.0, top_margin,
						"{0}: {1} (#{2})".format(title, owner, acct))

	# Post-header line
	p.line(left_margin, page_height - (1.25 * inch), right_margin, page_height - (1.25 * inch))

	# Draw body
	y_pos = page_height - 1.5 * inch
	for index, item in enumerate(items):
		height = y_pos - (index * 0.5 * inch)
		just_below = height - (0.1 * inch)
		item_string = "{0}: {1} ft^3 -- ${2}".format(item, item.volume, length(item.storage_fees, 2))
		p.drawString(left_margin, height, item_string)
		p.line(left_margin, just_below, right_margin, just_below)

	# Draw total cost
	y_below_items = y_pos - (len(items) * 0.5 * inch)
	p.drawString(left_margin, y_below_items, "Total cost: ${}".format(get_shipment_cost(shipid)))

	# Draw footer
	pageinfo = 'Virtual Warehouse Services'
	p.setFont('Helvetica', 9)
	p.drawString(left_margin, inch, pageinfo)
	p.drawString(left_margin, bottom_margin, "Generated at: {}".format(time_generated))

	p.showPage()
	p.save()

	response.write(temp.getvalue())
	return response