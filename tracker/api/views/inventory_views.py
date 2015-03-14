from django.http import Http404

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ..permissions import IsOwnerOrPrivileged
from ...models import Inventory
from ..serializers import InventorySerializer


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