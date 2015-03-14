from django.contrib.auth.models import User

from ..permissions import IsOwnerOrPrivileged
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ...models import Customer, Shipment, Inventory
from ..serializers import UserSerializer, InventorySerializer, \
    ShipmentSerializer, CustomerSerializer  # , CustomerModelSerializer


class ShipmentList(APIView):
    """
    List all shipments, or create a new shipment.
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get (self, request, format = None):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many = True)
        return Response(serializer.data)


class UserList(APIView):
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get (self, request, format = None):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True, context = {'request': request})
        return Response(serializer.data)


class CustomerList(APIView):
    """
    List all active Customers, or create a new one.
    """

    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get (self, request, format = None):
        # customers = Customer.objects.all()
        customers = Customer.objects.all().exclude(status = 0)
        serializer = CustomerSerializer(customers, many = True)
        # serializer = CustomerModelSerializer(customers, many = True)
        return Response(serializer.data)


class InventoryList(APIView):
    """
    List all items in storage
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @staticmethod
    def get (request, format = None):
        # inventory = Inventory.objects.all()
        inventory = Inventory.objects.all().exclude(status = 4)
        serializer = InventorySerializer(inventory, many = True)
        return Response(serializer.data)