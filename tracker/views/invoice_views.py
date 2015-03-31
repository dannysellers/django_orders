from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from .. import models
from ..pdf_utils.utils import render_report, render_report_second


def shipment_report (request, shipid):
    """
    Create a PDF for the shipment and return as an HTTP Response obj
    :param shipid: ID for the shipment
    :type shipid: int
    :return: Generated PDF
    """
    # TODO: Check to make sure the user is authenticated
    # Ultimately this should check for specific account authentication
    # Token authentication, or should it check that request.user == Shipment.owner?

    content_type = request.GET.get('type')

    if not request.user.is_anonymous():
        shipment = get_object_or_404(models.Shipment, shipid = shipid)
    else:
        return HttpResponseForbidden()

    # First method
    response = HttpResponse(content_type = 'application/pdf')
    _canvas, temp = render_report(shipment)

    # Second methd
    # response = render_report_second(shipment, request.user, content_type)

    # 'attachment' will prompt the user to download the file. 'inline'
    # will cause most modern browsers to display the PDF within the
    # browser window.
    response['Content-Disposition'] = '{0}; filename="Shipment_{1}_Invoice.pdf"'.format(content_type, shipid)

    response.write(temp.getvalue())
    return response


# def invoice_template (request, shipid):
#     context = RequestContext(request)
#
#     _shipment = models.Shipment.objects.get(shipid = shipid)
#     context_dict = dict(shipment = _shipment)
#
#     return render_to_response('tracker/invoice.html', context_dict, context)