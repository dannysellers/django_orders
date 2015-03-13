from django.contrib.auth.models import User

from rest_framework import status, permissions
from ..permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

from ...models import Customer, Shipment, Inventory
from ..serializers import UserSerializer, InventorySerializer, \
    ShipmentSerializer, CustomerSerializer  # , CustomerModelSerializer


class ShipmentList(APIView):
    """
    List all shipments, or create a new shipment.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get (self, request, format = None):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many = True)
        return Response(serializer.data)

    def post (self, request, format = None):
        serializer = ShipmentSerializer(data = request.data)
        if serializer.is_valid():
            print("Method to save called")
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def perform_create (self, serializer):
        # Pass the request's user to the serializer's
        # create method
        serializer.save(owner = self.request.user)


class UserList(APIView):
    def get (self, request, format = None):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True, context = {'request': request})
        return Response(serializer.data)

    def post (self, request, format = None):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def perform_create (self, serializer):
        # Pass the request's user to the serializer's
        # create method
        serializer.save(owner = self.request.user)


class CustomerList(APIView):
    """
    List all active Customers, or create a new one.
    """

    def get (self, request, format = None):
        # customers = Customer.objects.all()
        customers = Customer.objects.all().exclude(status = 0)
        serializer = CustomerSerializer(customers, many = True)
        # serializer = CustomerModelSerializer(customers, many = True)
        return Response(serializer.data)

    def post (self, request, format = None):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def perform_create (self, serializer):
        # Pass the request's user to the serializer's
        # create method
        serializer.save(owner = self.request.user)


class InventoryList(APIView):
    """
    List all items in storage
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    @staticmethod
    def get (request, format = None):
        # inventory = Inventory.objects.all()
        inventory = Inventory.objects.all().exclude(status = 4)
        serializer = InventorySerializer(inventory, many = True)
        return Response(serializer.data)