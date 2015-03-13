from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ..models import Customer, Shipment, Inventory


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


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
        depth = 1


# class CustomerModelSerializer(serializers.ModelSerializer):
#     shipments = ShipmentSerializer(many = True, read_only = True, required=False)

    # class Meta:
    #     model = Customer
    #     fields = ('shipments', 'name', 'acct', 'email')
    #     depth = 1


class CustomerSerializer(serializers.Serializer):
    @staticmethod
    def get_shipments(instance):
        # assert isinstance(instance, Customer)
        return [ShipmentSerializer(s).data for s in instance.shipment_set.all().exclude(status = 4)]

    @staticmethod
    def get_all_shipments(instance):
        return [ShipmentSerializer(s).data for s in instance.shipment_set.all()]

    def to_representation(self, instance):
        assert isinstance(instance, Customer)
        shipments = self.get_shipments(instance)
        return {
            'name': instance.name,
            'acct': instance.acct,
            'email': instance.email,
            'status': instance.get_status_display(),
            'shipments': shipments,
        }


class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required = False)  # May be a user with no Customer
    # customer = CustomerBaseSerializer()

    class Meta:
        model = User
        lookup_field = 'id'
        fields = ('username', 'email', 'groups', 'customer')
        # depth = 1
