from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import ExpiringTokenAuthentication
from ..permissions import IsOwnerOrPrivileged
from ...models import WorkOrder
from ..serializers import WorkOrderSerializer


class WorkOrderList(APIView):
    """
    List all work orders
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)

    @staticmethod
    def get(request, format = None):
        workorders = WorkOrder.objects.all().exclude()
        serializer = WorkOrderSerializer(workorders, many = True)
        return Response(serializer.data)


class WorkOrderDetail(APIView):
    """
    Get information about a WorkOrder object
    """
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication)

    def get(self, request, id, format = None):
        order = get_object_or_404(WorkOrder, pk = id)
        serializer = WorkOrderSerializer(order)
        return Response(serializer.data)
