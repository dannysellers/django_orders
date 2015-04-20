from django.contrib import admin
import models
from datetime import timedelta
from django.utils import timezone
# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

READ_ONLY_FIELDS_LABEL = "Read-only fields"


# Inline Displays
####################

class ShipmentInline(admin.TabularInline):
    model = models.Shipment

    fieldsets = [
        (None, {'fields': ['shipid', 'labor_time', 'tracking_number', 'palletized', 'status']}),
        (READ_ONLY_FIELDS_LABEL, {'fields': ['arrival', 'departure']}),
    ]
    readonly_fields = ('shipid', 'owner', 'arrival', 'departure')


class ItemOpInline(admin.TabularInline):
    model = models.ItemOperation

    fieldsets = [
        (None, {'fields': ['item', 'op_code', 'dt']})
    ]
    readonly_fields = ('item', 'op_code', 'dt')


class ShipOpInline(admin.TabularInline):
    model = models.ShipOperation

    fieldsets = [
        (None, {'fields': ['shipment', 'op_code', 'dt']})
    ]
    readonly_fields = ('shipment', 'op_code', 'dt')


# Model Admin Pages
###################

class ItemOpAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['item', 'op_code', 'dt']})
    ]
    list_display = ('item', 'op_code', 'dt')
    list_filter = ['op_code', 'item']
    readonly_fields = ('item', 'op_code', 'dt')


class ShipOpAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['shipment', 'op_code', 'dt']})
    ]
    list_display = ('shipment', 'op_code', 'dt')
    list_filter = ['op_code', 'shipment']
    readonly_fields = ('shipment', 'op_code', 'dt')


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['first_name', 'last_name', 'email', 'status']}),
        ('Account Information', {'fields': ['user', 'acct', 'notes'], 'classes': ['collapse']}),
        ('Dates', {'fields': ['createdate', 'closedate'], 'classes': ['collapse']})
    ]
    inlines = [ShipmentInline]
    readonly_fields = ('user', 'createdate', 'closedate', 'acct')
    list_display = ('acct', 'status', 'first_name', 'last_name', 'user')
    list_filter = ['status']
    search_fields = ['first_name', 'last_name', 'email', 'acct']


class ShipmentAdmin(admin.ModelAdmin):
    @staticmethod
    def has_workorder (instance):
        if instance.workorder.exists():
            return instance.workorder
        else:
            return False

    @staticmethod
    def inventory_count(instance):
        return instance.inventory.exclude(status = 4).count()

    fieldsets = [
        (None, {'fields': ['palletized', 'labor_time', 'tracking_number', 'status']}),
        ('Notes', {'fields': ['notes'], 'classes': ['collapse']}),
        (READ_ONLY_FIELDS_LABEL, {'fields': ['shipid', 'owner', 'arrival', 'departure'], 'classes': ['collapse']}),
    ]
    readonly_fields = ('shipid', 'owner', 'arrival', 'departure')
    inlines = [ShipOpInline]
    list_display = ('shipid', 'owner', 'inventory_count', 'has_workorder')
    list_filter = ['status']


class InventoryAdmin(admin.ModelAdmin):
    def bool_storage_fees (self, instance):
        if instance.get_storage_fees() == 0.00:
            return False
        else:
            return True

    fieldsets = [
        (None, {'fields': ['itemid', 'status', 'storage_fees', 'bool_storage_fees']}),
        ('Dimensions', {'fields': ['length', 'width', 'height', 'volume'], 'classes': ['collapse']}),
        (READ_ONLY_FIELDS_LABEL, {'fields': ['shipset', 'owner', 'arrival', 'departure']})
    ]
    readonly_fields = ('shipset', 'itemid', 'shipset', 'owner', 'arrival', 'departure', 'bool_storage_fees')
    list_display = ('itemid', 'shipset', 'owner', 'bool_storage_fees')
    inlines = [ItemOpInline]
    list_filter = ['status']  # , 'bool_storage_fees']

    bool_storage_fees.short_description = 'Storage fees?'


class WorkOrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['owner', 'shipment', 'contact_phone', 'contact_email']}),
        ('Details', {'fields': ['quantity', 'description', 'tracking'], 'classes': ['collapse']}),
        ('Extras', {'fields': ['gen_inspection', 'photo_inspection', 'item_count', 'bar_code_labeling', 'custom_boxing',
                               'consolidation', 'palletizing', 'misc_services', 'misc_service_text'],
                    'classes': ['collapse']})
    ]
    list_display = ('owner', 'shipment', 'quantity', 'createdate', 'status')
    readonly_fields = ('owner', 'createdate', 'finishdate')
    list_filter = ['status']


# class ExpiringTokenAdmin(TokenAdmin):
# def has_expired (self, instance):
#         """
#         If the token is more than 48 hours old, it is expired
#         """
#         now = timezone.now()
#         if instance.created < now - timedelta(hours = 48):
#             return True
#         else:
#             return False
#
#     list_display = ('key', 'user', 'created', 'has_expired')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Shipment, ShipmentAdmin)
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.ShipOperation, ShipOpAdmin)
admin.site.register(models.ItemOperation, ItemOpAdmin)
admin.site.register(models.WorkOrder, WorkOrderAdmin)
# TODO: Registering this customer Token model admin class required disabling rest_framework.authtoken.admin.TokenAdmin
# One alternative is to extend rest_framework.authtoken.models.Token
# admin.site.register(Token, ExpiringTokenAdmin)