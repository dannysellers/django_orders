from django.contrib.auth.models import User, Group
# from django.http import HttpResponse, Http404
# from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, permissions
from permissions import IsOwnerOrReadOnly
# from rest_framework.views import APIView
# from rest_framework.response import Response

from ..models import Customer, Shipment, Inventory
from serializers import UserSerializer, GroupSerializer, CustomerSerializer, InventorySerializer, ShipmentSerializer


# class ShipmentList(APIView):
#     """
#     List all shipments, or create a new shipment.
#     """
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def get (self, request, format = None):
#         shipments = Shipment.objects.all()
#         serializer = ShipmentSerializer(shipments, many = True)
#         return Response(serializer.data)
#
#     def post (self, request, format = None):
#         serializer = ShipmentSerializer(data = request.data)
#         if serializer.is_valid():
#             print("Method to save called")
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# class ShipmentDetail(APIView):
#     """
#     Retrieve, update, or delete a shipment instance.
#     """
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)
#
#     def get_object (self, pk):
#         try:
#             return Shipment.objects.get(shipid = pk)
#         except Shipment.DoesNotExist:
#             raise Http404
#
#     def get (self, request, pk, format = None):
#         shipment = self.get_object(pk)
#         serializer = ShipmentSerializer(shipment)
#         return Response(serializer.data)
#
#     def put (self, request, pk, format = None):
#         shipment = self.get_object(pk)
#         serializer = ShipmentSerializer(shipment, data = request.data)
#         if serializer.is_valid():
#             print("Method to save Shipment {} called".format(shipment.shipid))
#             return Response(serializer.data)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#
#     def delete (self, request, pk, format = None):
#         shipment = self.get_object(pk)
#         print("Method to delete Shipment {} called".format(shipment.shipid))
#         return Response(status = status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAdminUser,)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    # def perform_create(self, serializer):
    #     serializer.save(owner = self.request.user)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)