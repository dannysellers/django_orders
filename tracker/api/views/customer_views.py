from django.http import Http404

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from ..authentication import ExpiringTokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from ..serializers import CustomerSerializer
from ..permissions import IsOwnerOrPrivileged, IsOwnerOrPrivilegedObject
from ...models import Customer


class CustomerList(APIView):
    """
    List all active Customers, or create a new one.
    """

    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)

    def get (self, request, format = None):
        # customers = Customer.objects.all()
        customers = Customer.objects.all().exclude(status = 0)
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)


# class CustomerDetail(generics.RetrieveAPIView):
#     model = Customer
#     serializer_class = CustomerSerializer
#     permission_classes = (IsOwnerOrPrivileged,)
#     check_object_permissions = (IsOwnerOrPrivileged,)
#     authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)
#     queryset = Customer.objects.all()
#     lookup_field = 'acct'


class CustomerDetail(APIView):
    """
    Retrieve or update a Customer instance. Accounts cannot be deactivated
    via the API, and must be removed by an Operator or Admin.
    """
    permission_classes = (IsOwnerOrPrivilegedObject,)
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)

    @staticmethod
    def get_object (acct):
        try:
            return Customer.objects.get(acct = acct)
        except Customer.DoesNotExist:
            raise Http404

    def get (self, request, acct, format = None):
        customer = self.get_object(acct)
        serializer = CustomerSerializer(customer, context = {'request': request})
        return Response(serializer.data)

    # def put (self, request, acct, format = None):
    #     customer = self.get_object(acct)
    #     serializer = CustomerSerializer(customer, data = request.data)
    #     # serializer = CustomerSerializer(customer, data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    #
    # def perform_create (self, serializer):
    #     # Pass the request's user to the serializer's
    #     # create method
    #     serializer.save(owner = self.request.user)