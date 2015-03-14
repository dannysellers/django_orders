from django.http import Http404

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from ..serializers import ShipmentSerializer
from ..permissions import IsOwnerOrPrivileged
from ...models import Shipment


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