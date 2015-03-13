from django.contrib.auth.models import User  # , Group
from django.http import Http404

from rest_framework import permissions, status  # , mixins, generics
from ..permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ...models import Customer, Shipment, Inventory
from ..serializers import UserSerializer, InventorySerializer, \
    ShipmentSerializer, CustomerSerializer  # , CustomerModelSerializer


class ShipmentDetail(APIView):
    """
    Retrieve, update, or delete a Shipment instance.
    """
    # TODO: Investigate Mixins & generics.GenericAPIView
    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
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

    def delete (self, request, shipid, format = None):
        shipment = self.get_object(shipid)
        shipment.set_status(4)
        return Response(status = status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
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
    Retrieve, update, or delete a Customer instance
    """

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

    def delete (self, request, acct, format = None):
        customer = self.get_object(acct)
        customer.close_account()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def perform_create (self, serializer):
        # Pass the request's user to the serializer's
        # create method
        serializer.save(owner = self.request.user)


class InventoryDetail(APIView):
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