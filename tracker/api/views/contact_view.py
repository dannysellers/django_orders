from django.core.mail import send_mail
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions

import smtplib


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_us (request):
    """

    """
    if request.method != 'POST':
        return Response(status = status.HTTP_400_BAD_REQUEST)
    else:
        contact_dict = dict()
        for key, value in request.POST.iteritems():
            contact_dict[key] = value

        try:
            send_mail(subject = "Someone has contacted you!",
                      message = "Someone has contacted us from the website.\nThey are:\n\tPhone:\t{}\n\tEmail:\t{}\n\tMessage:{}".format(
                          contact_dict['phone'], contact_dict['email'], contact_dict['message']),
                      from_email = contact_dict['email'],
                      recipient_list = settings.EMAIL_LIST,
                      auth_user = settings.EMAIL_HOST_USER,
                      auth_password = settings.EMAIL_HOST_PASSWORD)
        except smtplib.SMTPException as e:
            return Response(data = {'message': "Error sending message: {}".format(e)},
                            status = status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(data = {'message': 'Message sent successfully.'},
                    status = status.HTTP_200_OK)
