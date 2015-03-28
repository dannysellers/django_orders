try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import os

from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm, toLength
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image, Frame, PageTemplate

from .. import models
from ..templatetags.num_filters import length
from ..utils import get_shipment_cost
from ..pdf_utils import helpers


def shipment_report (request, shipid):
    """
    Create a PDF for the shipment and return as an HTTP Response obj
    :param shipid: ID for the shipment
    :type shipid: int
    :return: Generated PDF
    """

    # TODO: Check for token authentication before retrieving shipment

    content_type = request.GET.get('type')

    response = HttpResponse(content_type = 'application/pdf')

    shipment = get_object_or_404(models.Shipment, shipid = shipid)
    owner = str(shipment.owner.name)
    acct = str(shipment.owner.acct)
    items = shipment.inventory.all()
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


def shipment_invoice (request, shipid):
    """
    Generate a PDF with the contents of the given shipment
    """
    # Check to make sure the user is authenticated
    # Ultimately this should check for specific account authentication
    # Token authentication, or should it check that request.user == Shipment.owner?
    content_type = request.GET.get('type')

    if not request.user.is_anonymous():
        try:
            shipment = models.Shipment.objects.get(shipid = shipid)
        except models.Shipment.DoesNotExist:
            raise Http404
    else:
        return HttpResponseForbidden()

    # Create the response with the appropriate headers
    response = HttpResponse(content_type = 'application/pdf')

    # Create the PDF object, using the response as the "file"
    doc = SimpleDocTemplate(response,
                            pagesize = A4,
                            leftMargin = inch,
                            rightMargin = inch,
                            topMargin = 0.75 * inch,
                            bottomMargin = 0.75 * inch,
                            title = 'Shipment {} Invoice'.format(shipid),
                            subject = 'Invoice for {}'.format(request.user.username))

    # Container for 'flowable' objects
    elements = []

    # Create two frames
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 2 - 6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + doc.width / 2 + 6, doc.bottomMargin, doc.width / 2 - 6, doc.height, id='col2')

    # Set the title
    # This looks for logo.jpg in the /views folder. Better handling of this to come...
    logo = Image(os.path.join(os.path.dirname(__file__), 'logo.jpg'),
                 width = 2.5 * inch,
                 height = 0.8 * inch)
    elements.append(logo)
    elements.append(Spacer(10 * inch, doc.height))

    p = Paragraph('<para align="center"><strong>{}</strong></para>'.format(shipment),
                  helpers.styleSheet['HeaderBold'])
    elements.append(p)
    elements.append(Spacer(10 * inch, 0.5 * inch))

    # Iterate through the Shipment and render each Item
    for item in shipment.inventory.all():
        elements.append(helpers.render_inventory(item))
        elements.append(Spacer(10 * inch, 0.5 * inch))

    # Footer, date, and info
    elements.append(Spacer(10 * inch, 0.5 * inch))
    # elements.append(helpers.render_footer(request.build_absolute_uri(shipment.get_absolte_url())))

    # doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2]), ])

    # Write the document and send the response to the browser
    doc.build(elements)

    # Create the HttpResponse obj with appropriate PDF headers
    if content_type:
        response['Content-Disposition'] = '{0}; filename="Shipment_{1}_Invoice.pdf"'.format(content_type, shipid)
    else:
        response['Content-Disposition'] = 'attachment; filename="Shipment_{0}_Invoice.pdf"'.format(shipid)

    response['Content-Length'] = len(response.content)
    return response


# def invoice_template (request, shipid):
#     context = RequestContext(request)
#
#     _shipment = models.Shipment.objects.get(shipid = shipid)
#     context_dict = dict(shipment = _shipment)
#
#     return render_to_response('tracker/invoice.html', context_dict, context)