from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings

from .. import models
from selenium import webdriver

import cStringIO
from xhtml2pdf import pisa
import os
import logging

logging.basicConfig()


@login_required
def shipment_report (request, shipid, content_type):
    """
    Create a PDF for the shipment and return as an HTTP Response obj
    :param shipid: ID for the shipment
    :type shipid: int
    :return: Generated PDF
    """
    # TODO: Check to make sure the user is authenticated
    # Ultimately this should check for specific account authentication
    # Token authentication, or should it check that request.user == Shipment.owner?

    def write_img_to_pdf (src, dest):
        # Helper xhtml2pdf function to dump image/template to pdf
        context = dict(img_path = src)
        template = get_template('tracker/pdf_img_template.html')
        html = template.render(Context(context))

        with open(dest, 'wb') as f:
            pisa.pisaDocument(cStringIO.StringIO(
                html.encode('UTF-8')), f
            )

    if not request.user.is_anonymous():
        shipment = get_object_or_404(models.Shipment, shipid = shipid)
    else:
        return HttpResponseForbidden()

    phantom = webdriver.PhantomJS()
    legend_url = 'http://' + request.get_host() + reverse('invoice_template', kwargs = {'shipid': shipment.shipid})
    phantom.get(legend_url)

    legend_path = os.path.join(settings.STATIC_ROOT,
                               'tracker/static/tmp',
                               'shipment-{}-invoice.png'.format(shipment.shipid))
    legend_pdf_path = os.path.join(settings.STATIC_ROOT,
                                   'tracker/static/tmp',
                                   'shipment-{}-invoice.pdf'.format(shipment.shipid))
    created_files = [legend_path, legend_pdf_path]

    phantom.get_screenshot_as_file(legend_path)
    write_img_to_pdf(legend_path, legend_pdf_path)

    response = HttpResponse(content_type = 'application/pdf')

    with open(legend_pdf_path, 'rb') as f:
        buf = cStringIO.StringIO(f.read())

    # clean up temp files
    for path in created_files:
        if os.path.exists(path):
            os.remove(path)

    response.content = buf.getvalue()
    # 'attachment' will prompt the user to download the file. 'inline'
    # will cause most modern browsers to display the PDF within the
    # browser window.
    response['Content-Disposition'] = '{0}; filename="Shipment_{1}_Invoice.pdf"'.format(content_type, shipid)
    return response


def invoice_template (request, shipid):
    """
    Fxn to display the template to be rendered by xhtml2pdf
    """

    _shipment = models.Shipment.objects.get(shipid = shipid)
    context_dict = dict(shipment = _shipment,
                        now = timezone.now())

    return render(request, 'tracker/invoice.html', context_dict)