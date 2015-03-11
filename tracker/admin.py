from django.contrib import admin
import models

READ_ONLY_FIELDS_LABEL = "Read-only fields"
# TODO: Add Grappelli project (https://github.com/sehmaschine/django-grappelli)


class ShipmentInline(admin.TabularInline):
    model = models.Shipment

    fieldsets = [
        (None, {'fields': ['shipid', 'labor_time', 'tracking_number', 'palletized', 'status']}),
        (READ_ONLY_FIELDS_LABEL, {'fields': ['arrival', 'departure']}),
    ]
    readonly_fields = ('shipid', 'owner', 'arrival', 'departure')


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'email', 'status']}),
        ('Account Information', {'fields': ['acct', 'notes'], 'classes': ['collapse']}),
        (READ_ONLY_FIELDS_LABEL, {'fields': ['createdate', 'closedate'], 'classes': ['collapse']})
    ]
    inlines = [ShipmentInline]
    readonly_fields = ('createdate', 'closedate')
    list_display = ('acct', 'name')
    list_filter = ['status']
    search_fields = ['name', 'email', 'acct']


class ItemOpInline(admin.TabularInline):
    model = models.ItemOperation

    fieldsets = [
        (None, {'fields': ['item', 'op_code', 'dt']})
    ]
    readonly_fields = ('item', 'op_code', 'dt')


class ItemOpAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['item', 'op_code', 'dt']})
    ]
    readonly_fields = ('item', 'op_code', 'dt')


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


class ShipOpInline(admin.TabularInline):
    model = models.ShipOperation

    fieldsets = [
        (None, {'fields': ['shipment', 'op_code', 'dt']})
    ]
    readonly_fields = ('shipment', 'op_code', 'dt')


class ShipOpAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['shipment', 'op_code', 'dt']})
    ]
    readonly_fields = ('shipment', 'op_code', 'dt')


class ShipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['palletized', 'labor_time', 'tracking_number', 'status']}),
        ('Notes', {'fields': ['notes'], 'classes': ['collapse']}),
        (READ_ONLY_FIELDS_LABEL, {'fields': ['shipid', 'owner', 'arrival', 'departure'], 'classes': ['collapse']}),
    ]
    readonly_fields = ('shipid', 'owner', 'arrival', 'departure')
    inlines = [ShipOpInline]
    list_display = ('shipid', 'owner')
    list_filter = ['status']


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Shipment, ShipmentAdmin)
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.ShipOperation, ShipOpAdmin)
admin.site.register(models.ItemOperation, ItemOpAdmin)
