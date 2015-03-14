from django.contrib.auth.models import User  # , Group
from django.http import Http404

from rest_framework import status  # , mixins, generics
from ..permissions import IsOwnerOrPrivileged
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ...models import Customer, Shipment, Inventory
from ..serializers import UserSerializer, InventorySerializer, \
    ShipmentSerializer, CustomerSerializer  # , CustomerModelSerializer


class ShipmentDetail(APIView):
    """
    Retrieve a Shipment instance.
    """
    # TODO: Investigate Mixins & generics.GenericAPIView
    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @staticmethod
    def get_object (shipid):
        try:
            return Shipment.objects.get(shipid = shipid)
        except Shipment.DoesNotExist:
            raise Http404

    def get (self, request, shipid, format = None):
        shipment = self.get_object(shipid)
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve or update a User instance. Users cannot be destroyed or
    deactivated via the API, and must be removed by an Operator or Admin.
    """
    permission_classes = (IsOwnerOrPrivileged,)
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


class CustomerDetail(APIView):
    """
    Retrieve or update a Customer instance. Accounts cannot be deactivated
    via the API, and must be removed by an Operator or Admin.
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @staticmethod
    def get_object (acct):
        try:
            return Customer.objects.get(acct = acct)
        except Customer.DoesNotExist:
            raise Http404

    def get (self, request, acct, format = None):
        customer = self.get_object(acct)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put (self, request, acct, format = None):
        customer = self.get_object(acct)
        serializer = CustomerSerializer(customer, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def perform_create (self, serializer):
        # Pass the request's user to the serializer's
        # create method
        serializer.save(owner = self.request.user)


class InventoryDetail(APIView):
    """
    Get information about an Inventory object.
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @staticmethod
    def get_object (itemid):
        try:
            return Inventory.objects.get(itemid = itemid)
        except Inventory.DoesNotExist:
            raise Http404

    def get (self, request, itemid, format = None):
        item = self.get_object(itemid)
        serializer = InventorySerializer(item)
        return Response(serializer.data)