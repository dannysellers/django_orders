from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django.utils.translation import ugettext_lazy as _
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers, exceptions
# from authentication import ExpiringTokenAuthentication
from ..models import Customer, Shipment, Inventory
from rest_framework.authtoken.models import Token


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('itemid', 'volume', 'get_storage_fees', 'status')


class ShipmentSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many = True)

    class Meta:
        model = Shipment
        fields = ('shipid', 'labor_time', 'status', 'storage_fees', 'inventory')


class CustomerSerializer(serializers.ModelSerializer):
    shipments = ShipmentSerializer(many = True)

    class Meta:
        model = Customer
        fields = ('name', 'acct', 'shipments')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    # customer = serializers.PrimaryKeyRelatedField(read_only = True)
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