from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ..models import Customer, Shipment, Inventory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'acct', 'email')


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment
        fields = ('owner', 'shipid', 'labor_time', 'status', 'storage_fees')


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inventory
        fields = ('owner', 'shipset', 'itemid', 'volume', 'get_storage_fees', 'status')