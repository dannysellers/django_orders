from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import ExpiringTokenAuthentication
from ..permissions import IsOwnerOrPrivileged
from ...models import Inventory
from ..serializers import InventorySerializer


class InventoryList(APIView):
    """
    List all items in storage
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)

    @staticmethod
    def get (request, format = None):
        # inventory = Inventory.objects.all()
        inventory = Inventory.objects.all().exclude(status = 4)
        serializer = InventorySerializer(inventory, many = True)
        return Response(serializer.data)


class InventoryDetail(APIView):
    """
    Get information about an Inventory object.
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)

    def get (self, request, itemid, format = None):
        item = get_object_or_404(Inventory, pk = itemid)
        serializer = InventorySerializer(item)
        return Response(serializer.data)
