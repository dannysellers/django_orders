from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django.utils.translation import ugettext_lazy as _
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers, exceptions
# from authentication import ExpiringTokenAuthentication
from ..models import Customer, Shipment, Inventory, OptExtras, WorkOrder
from rest_framework.authtoken.models import Token


class ExtrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptExtras
        fields = ('quantity', 'unit_cost', 'total_cost', 'description')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('itemid', 'volume', 'storage_fees', 'get_storage_fees', 'status_text')


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ('id', 'tracking', 'gen_inspection', 'photo_inspection', 'item_count',
                  'bar_code_labeling', 'custom_boxing', 'consolidation', 'palletizing',
                  'misc_services', 'misc_service_text', 'status_text', 'createdate', 'finishdate')


class ShipmentSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many = True)
    extras = ExtrasSerializer(many = True)
    workorder = WorkOrderSerializer(many = False)

    class Meta:
        model = Shipment
        fields = ('shipid', 'labor_time', 'get_status_display', 'storage_fees', 'inventory',
                  'extras', 'workorder')


class CustomerSerializer(serializers.ModelSerializer):
    shipments = ShipmentSerializer(many = True)

    class Meta:
        model = Customer
        fields = ('name', 'acct', 'createdate', 'shipments')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'customer')
        extra_kwargs = {'url': {'lookup_field': 'id'}}


# class ExpiringAuthTokenSerializer(AuthTokenSerializer):
#
# def is_valid(self, raise_exception=False):
#         if 'username' in self.initial_data and 'password' in self.initial_data:
#             username = self.initial_data['username']
#             password = self.initial_data['password']
#             auth = self.validate({'username': username, 'password': password})
#             return auth
#         elif 'token' in self.initial_data:
#             _token = self.initial_data['token']
#             user, token = ExpiringTokenAuthentication.authenticate_credentials(key = token)
#             if user:
#                 return True


class CustomTokenSerializer(serializers.ModelSerializer):
    """
    Custom token serializer that includes user ID
    """

    class Meta:
        model = Token
        fields = ('key', 'user')
