from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta

from audit_log.models import AuthStampedModel
from audit_log.models.managers import AuditLog

from .managers import CustomerManager, ShipmentManager, InventoryManager, \
    ItemOpManager, ShipOpManager, OptExtraManager

UNIT_STORAGE_FEE = 0.10

CUSTOMER_STATUS_CODES = (
    ('0', 'Inactive'),
    ('1', 'Active'),
)

INVENTORY_STATUS_CODES = (
    ('0', 'Inducted'),
    ('1', 'Order received'),
    ('2', 'Order started'),
    ('3', 'Order completed'),
    ('4', 'Shipped'),
)


class Customer(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length = 128, unique = False)
    acct = models.IntegerField(max_length = 5, primary_key = True, unique = True)
    # TODO: Add hidden account ID so that the front-facing one can be changed?
    email = models.EmailField()
    status = models.CharField(max_length = 1, choices = CUSTOMER_STATUS_CODES)
    createdate = models.DateField()
    closedate = models.DateField(null = True)
    notes = models.TextField()

    objects = CustomerManager()

    def __unicode__ (self):
        return '{}: {}'.format(self.acct, self.name)

    @property
    def storage_fees (self):
        fees = 0.00
        for item in self.inventory_set.exclude(status = 4):
            fees += item.get_storage_fees()
        return fees


class Shipment(AuthStampedModel):
    owner = models.ForeignKey(Customer)
    shipid = models.IntegerField(unique = True)
    palletized = models.BooleanField(default = False)
    arrival = models.DateField()
    departure = models.DateField(null = True)
    labor_time = models.IntegerField()
    notes = models.TextField(null = True)
    tracking_number = models.CharField(max_length = 30, null = True)
    status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

    objects = ShipmentManager()
    audit_log = AuditLog()

    def __unicode__ (self):
        return 'Acct #{}, Shipment {}'.format(self.owner.acct, self.shipid)

    @property
    def storage_fees (self):
        fees = 0.00
        for item in self.inventory_set.exclude(status = 4):
            fees += item.get_storage_fees()
        return fees


@receiver(post_save, sender = Shipment)
def ship_op_signal (sender, instance, **kwargs):
    # TODO: These post_save methods are called 3 times on creation (audit_log, probably)
    # Convert to middleware?
    ShipOperation.objects.create_operation(shipment = instance,
                                           op_code = instance.status)


class Inventory(AuthStampedModel):
    shipset = models.ForeignKey(Shipment)
    owner = models.ForeignKey(Customer)
    itemid = models.IntegerField(unique = True, primary_key = True)
    length = models.FloatField(default = 1.00, max_length = 5)
    width = models.FloatField(default = 1.00, max_length = 5)
    height = models.FloatField(default = 1.00, max_length = 5)
    volume = models.FloatField(default = 1.00, max_length = 5)
    storage_fees = models.FloatField(default = UNIT_STORAGE_FEE)
    status = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)
    arrival = models.DateField()
    departure = models.DateField(null = True)

    objects = InventoryManager()
    audit_log = AuditLog()

    def __unicode__ (self):
        return 'Item {}'.format(self.itemid)

    def get_storage_fees (self):
        if self.status != 4 and timezone.now().date() - self.arrival >= timedelta(days = 10):
            return self.storage_fees
        else:
            return 0.00

    class Meta:
        verbose_name_plural = 'inventory'


@receiver(post_save, sender = Inventory)
def item_op_signal (sender, instance, **kwargs):
    ItemOperation.objects.create_operation(item = instance,
                                           op_code = instance.status)


class Operation(AuthStampedModel):
    """
    Base class for ShipOperation and ItemOperation, the
    only difference between which is the ForeignKey relation
    """
    dt = models.DateTimeField()
    op_code = models.CharField(max_length = 1, choices = INVENTORY_STATUS_CODES, default = 0)

    class Meta:
        abstract = True


class ShipOperation(Operation):
    shipment = models.ForeignKey(Shipment)

    objects = ShipOpManager()

    class Meta:
        verbose_name = "shipment operation"

    def __unicode__ (self):
        return 'Item {}, Code {}'.format(self.shipment.shipid, self.op_code)


class ItemOperation(Operation):
    item = models.ForeignKey(Inventory)

    objects = ItemOpManager()

    def __unicode__ (self):
        return 'Item {}, Code {}'.format(self.item.itemid, self.op_code)


class OptExtras(models.Model):
    shipment = models.ForeignKey(Shipment)
    quantity = models.IntegerField(default = 1)
    unit_cost = models.FloatField()
    total_cost = models.FloatField()
    description = models.TextField()

    objects = OptExtraManager()

    def __unicode__ (self):
        return '{} x {}: ${}'.format(self.quantity, self.description, self.unit_cost)