# import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from models import Shipment

from templatetags.num_filters import length
from utils import get_shipment_cost


def shipment_report (request, shipid):
	"""
	Create a PDF for the shipment and return as an HTTP Response obj
	:param shipid: ID for the shipment
	:type shipid: int
	:return: Generated PDF
	"""
	content_type = request.GET.get('type')

	response = HttpResponse(mimetype = 'application/pdf')

	shipment = get_object_or_404(Shipment, shipid = shipid)
	owner = str(shipment.owner.name)
	acct = str(shipment.owner.acct)
	items = shipment.inventory_set.all()
	time_generated = str(timezone.now())

	# 'attachment' will prompt the user to download the file. 'inline'
	# will cause most modern browsers to display the PDF within the
	# browser window.
	response['Content-Disposition'] = '{0}; filename="Shipment_{1}_Invoice.pdf"'.format(content_type, shipid)

	# Page setup
	p = canvas.Canvas(response)
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

	return response