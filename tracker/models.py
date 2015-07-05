from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta, date

from audit_log.models import AuthStampedModel
from audit_log.models.managers import AuditLog

from .managers import CustomerManager, ShipmentManager, InventoryManager, \
    ItemOpManager, ShipOpManager, OptExtraManager, WorkOrderManager, \
    WorkOrderOpManager

UNIT_STORAGE_FEE = 0.10
STORAGE_FEES_DAYS = 10

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
    # Status codes above 1 digit length are
    # only used for Work Orders & WorkOrderOps
    ('999', 'Terminated'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank = True)
    first_name = models.CharField(max_length = 128, unique = False)
    last_name = models.CharField(max_length = 128, unique = False)
    acct = models.IntegerField(max_length = 5, primary_key = True, unique = True)
    # TODO: Add hidden account ID so that the front-facing one can be changed?
    # TODO: Email field necessary given email field on User?
    email = models.EmailField()
    status = models.CharField(max_length = 1, choices = CUSTOMER_STATUS_CODES)
    createdate = models.DateField()
    closedate = models.DateField(null = True)
    notes = models.TextField()

    objects = CustomerManager()

    def __unicode__ (self):
        return '{}: {}'.format(self.acct, self.name)

    @property
    def name (self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def storage_fees (self):
        fees = 0.00
        for item in self.inventory.exclude(status = 4):
            fees += item.get_storage_fees()
        return fees

    @property
    def is_active (self):
        if self.status == 0:
            return False
        else:
            return True

    def close_account (self):
        # TODO: Should this alter statuses of any existing Shipments & Inventory?
        self.closedate = date.today()
        self.status = 0
        self.save()


class Shipment(AuthStampedModel):
    owner = models.ForeignKey(Customer, related_name = 'shipments')
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
        # return 'Acct #{}, Shipment {}'.format(self.owner.acct, self.shipid)
        return 'Shipment #{}: {}'.format(self.shipid, self.arrival)

    @property
    def workorder(self):
        if self._workorder.exists() and self._workorder.count() == 1:
            return self._workorder.first()
        elif self._workorder.count() > 1:
            # TODO: Raise exception?
            pass
        else:
            return None

    def storage_fees (self):
        fees = 0.00
        for item in self.inventory.exclude(status = 4):
            fees += item.get_storage_fees()
        return fees

    def set_status (self, status):
        for item in self.inventory.all():
            item.status = status
            if status == 4:
                item.departure = date.today()
            item.save()
        self.status = status
        if status == 4:
            self.departure = date.today()
        return True


@receiver(post_save, sender = Shipment)
def ship_op_signal (sender, instance, **kwargs):
    # TODO: These post_save methods are called 3 times on creation (audit_log, probably)
    # Convert to middleware?
    ShipOperation.objects.create_operation(shipment = instance,
                                           op_code = instance.status)
    if instance.workorder:
        # Update the Work Order along with the Shipment
        WorkOrderOperation.objects.create_operation(order = instance.workorder,
                                                    op_code = instance.status)


class Inventory(AuthStampedModel):
    shipset = models.ForeignKey(Shipment, related_name = 'inventory')
    owner = models.ForeignKey(Customer, related_name = 'inventory')
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
        age = timezone.now().date() - self.arrival
        if self.status != 4 and age >= timedelta(days = STORAGE_FEES_DAYS):
            return self.storage_fees
        else:
            return 0.00

    @property
    def status_text (self):
        return self.get_status_display()

    @property
    def get_total_fees (self):
        """
        Returns the total amount in fees an item has incurred
        during its time in storage
        """
        if not self.shipset.departure or not self.departure:
            return 0.00
        else:
            days = (self.departure - self.arrival).days - STORAGE_FEES_DAYS
            return self.storage_fees * days

    class Meta:
        verbose_name_plural = 'inventory'


@receiver(post_save, sender = Inventory)
def item_op_signal (sender, instance, **kwargs):
    ItemOperation.objects.create_operation(item = instance,
                                           op_code = instance.status)


class OptExtras(models.Model):
    shipment = models.ForeignKey(Shipment, related_name = 'extras')
    quantity = models.IntegerField(default = 1)
    unit_cost = models.FloatField()
    total_cost = models.FloatField()
    description = models.TextField()

    objects = OptExtraManager()

    def __unicode__ (self):
        return '{} x {}: ${}'.format(self.quantity, self.description, self.unit_cost)


class WorkOrder(AuthStampedModel):
    owner = models.ForeignKey(Customer, related_name = 'workorders')
    # Work orders should correspond to a given Shipment, but an
    # order may be received prior to the creation of a Shipment.
    # A OneToOneField was too restrictive, prohibited Shipments from
    # being created without any WorkOrder. The workorder property
    # mimics the behavior of a singleton ForeignKey
    shipment = models.ForeignKey(Shipment, null = True, blank = True, unique = True, related_name = '_workorder')
    contact_phone = models.CharField(max_length = 20)
    contact_email = models.EmailField(max_length = 254)
    quantity = models.IntegerField(max_length = 4, default = 1)
    description = models.TextField()
    tracking = models.CharField(max_length = 50)
    # Services desired
    gen_inspection = models.BooleanField(default = False, help_text = "General inspection")
    photo_inspection = models.BooleanField(default = False, help_text = "Photographic inspection")
    item_count = models.BooleanField(default = False, help_text = "Count of items")
    bar_code_labeling = models.BooleanField(default = False, help_text = "FNSKU / Bar code labeling")
    custom_boxing = models.BooleanField(default = False, help_text = "Custom product boxing")
    consolidation = models.BooleanField(default = False, help_text = "Consolidation / repacking")
    palletizing = models.BooleanField(default = False, help_text = "Palletizing")
    misc_services = models.BooleanField(default = False, help_text = "Additional miscellaneous services")
    misc_service_text = models.CharField(max_length = 1000, help_text = "Add'l misc service description")
    status = models.CharField(max_length = 3, choices = INVENTORY_STATUS_CODES, default = 0)
    createdate = models.DateTimeField(default = timezone.now())
    finishdate = models.DateTimeField(null = True, blank = True)

    objects = WorkOrderManager()
    audit_log = AuditLog()

    def __unicode__ (self):
        # return 'Order {}: {}'.format(self.pk, self.owner.acct)
        return 'Order #{}: {}'.format(self.pk, self.createdate)

    @property
    def status_text (self):
        return self.get_status_display()

    def remove_order (self):
        """
        Fxn to remove work orders (i.e. duplicate submissions) while
        preserving their record
        """
        if self.shipment:
            self.shipment = None
        self.finishdate = timezone.now()
        self.description += "\nOrder terminated on " + str(self.finishdate)
        self.status = '999'
        self.save()


@receiver(post_save, sender = WorkOrder)
def workorder_op_signal (sender, instance, **kwargs):
    WorkOrderOperation.objects.create_operation(order = instance,
                                                op_code = instance.status)


class Operation(AuthStampedModel):
    """
    Base class for ShipOperation and ItemOperation, the
    only difference between which is the ForeignKey relation
    """
    dt = models.DateTimeField()
    op_code = models.CharField(max_length = 3, choices = INVENTORY_STATUS_CODES, default = 0)

    class Meta:
        abstract = True


class ShipOperation(Operation):
    shipment = models.ForeignKey(Shipment, related_name = 'operations')

    objects = ShipOpManager()

    class Meta:
        verbose_name = "shipment operation"

    def __unicode__ (self):
        return 'Shipment {}, {}'.format(self.shipment.shipid, self.get_op_code_display())


class ItemOperation(Operation):
    item = models.ForeignKey(Inventory, related_name = 'operations')

    objects = ItemOpManager()

    class Meta:
        verbose_name = "item operation"

    def __unicode__ (self):
        return 'Item {}, {}'.format(self.item.itemid, self.get_op_code_display())


class WorkOrderOperation(Operation):
    order = models.ForeignKey(WorkOrder, related_name = 'operations')

    objects = WorkOrderOpManager()

    class Meta:
        verbose_name = "work order operation"

    def __unicode__ (self):
        return 'Order {}, {}'.format(self.order.id, self.get_op_code_display())
