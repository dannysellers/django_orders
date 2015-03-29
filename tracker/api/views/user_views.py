from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer
from ..permissions import IsOwnerOrPrivileged, IsOwnerOrPrivilegedObject
from ...models import Customer


class UserList(APIView):
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get (self, request, format = None):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True, context = {'request': request})
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve or update a User instance. Users cannot be destroyed or
    deactivated via the API, and must be removed by an Operator or Admin.
    """
    permission_classes = (IsOwnerOrPrivilegedObject,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @staticmethod
    def get_object (pk):
        try:
            return User.objects.get(id = pk)
        except User.DoesNotExist:
            raise Http404

    def get (self, request, pk, format = None):
        user = self.get_object(pk)
        # serializer = UserSerializer(user)
        serializer = UserSerializer(user,
                                    context = {'request': request})
        return Response(serializer.data)

    def put (self, request, pk, format = None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def receive_work_order (request, acct):
    """
    Receives POSTed work order form. At the moment, it just sends us an email,
    but ultimately I'll construct a WorkOrder model to be displayed on the site
    """
    if request.method != 'POST':
        return Response(status = status.HTTP_400_BAD_REQUEST)
    else:
        try:
            customer = Customer.objects.get(acct = acct)
        except Customer.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        _subject = "Order received from #{} ({})".format(customer.acct, customer.name)
        _message = ""

        _from_email = request.POST['email']
        # Form elements
        try:
            send_mail(subject = _subject,
                      message = _message,
                      from_email = _from_email,
                      recipient_list = [settings.EMAIL_HOST_USER],
                      auth_user = settings.EMAIL_HOST_USER,
                      auth_password = settings.EMAIL_HOST_PASSWORD,
                      fail_silently = False)
        except:
            # log error
            # try sending an email via Mandrill
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status = status.HTTP_200_OK)
