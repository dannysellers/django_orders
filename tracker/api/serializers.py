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
        # fields = ('itemid', 'volume', 'get_storage_fees', 'status')
        fields = ('owner', 'shipset', 'itemid', 'volume', 'get_storage_fees', 'status')


class ShipmentSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many = True, read_only = True)

    class Meta:
        model = Shipment
        fields = ('shipid', 'labor_time', 'status', 'storage_fees', 'inventory')
        # fields = ('owner', 'shipid', 'labor_time', 'status', 'storage_fees', 'inventory')
        # depth = 1


class CustomerModelSerializer(serializers.ModelSerializer):
    # shipments = serializers.HyperlinkedRelatedField(view_name = 'shipment_detail',
    #                                                 lookup_field = 'shipid',
    #                                                 read_only = True)

    class Meta:
        model = Customer
        fields = ('name', 'acct', 'email') # , 'shipments')
        depth = 1


class CustomerSerializer(serializers.Serializer):
    @staticmethod
    def get_shipments(instance):
        # assert isinstance(instance, Customer)
        return [ShipmentSerializer(s).data for s in instance.shipment_set.all().exclude(status = 4)]

    @staticmethod
    def get_all_shipments(instance):
        return [ShipmentSerializer(s).data for s in instance.shipment_set.all()]

    def to_representation(self, instance):
        # assert isinstance(instance, Customer)
        shipments = self.get_shipments(instance)
        return {
            'name': instance.name,
            'acct': instance.acct,
            'email': instance.email,
            'status': instance.get_status_display(),
            'shipments': shipments,
        }

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    # customer = CustomerModelSerializer(required = False)  # May be a user with no Customer
    customer = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'customer')
        extra_kwargs = {'url': {'lookup_field': 'id'}}
        # depth = 1


# class ExpiringAuthTokenSerializer(AuthTokenSerializer):
#
#     def is_valid(self, raise_exception=False):
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