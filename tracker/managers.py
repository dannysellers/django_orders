from datetime import date

from django.db.models import Manager
from django.utils import timezone
from django.contrib.auth.models import User, Group


class CustomerManager(Manager):
    def create_customer (self, first_name, last_name, email, acct, password=None):
        if not password:
            password = User.objects.make_random_password()

        customer_group, created = Group.objects.get_or_create('Customer')

        # TODO: Allow username as login instead of email?
        _user = User.objects.create_user(first_name = first_name,
                                         last_name = last_name,
                                         username = email,
                                         email = email,
                                         password = password)
        # Set permissions
        _user.groups.add(customer_group)

        _customer = self.create(user = _user, first_name = first_name,
                                last_name = last_name, email = email,
                                createdate = date.today(), status = 1,
                                notes = "notes", acct = int(acct))
        return _customer


class ShipmentManager(Manager):
    def create_shipment (self, owner, palletized, labor_time, notes, tracking_number):
        from models import Shipment

        shipid = Shipment.objects.count() + 1
        arrival = date.today()
        status = 0
        _shipment = self.create(owner = owner, shipid = shipid, palletized = palletized,
                                arrival = arrival, labor_time = labor_time, notes = notes,
                                tracking_number = tracking_number, status = status)
        return _shipment


class InventoryManager(Manager):
    def create_inventory (self, shipset, length, width, height):
        from models import Inventory, UNIT_STORAGE_FEE

        itemid = Inventory.objects.count() + 1
        owner = shipset.owner
        arrival = shipset.arrival
        volume = float(length) * float(width) * float(height)
        storage_fees = volume * UNIT_STORAGE_FEE
        status = 0
        _item = self.create(itemid = itemid, shipset = shipset, length = length,
                            width = width, height = height,
                            owner = owner, arrival = arrival,
                            volume = volume, storage_fees = storage_fees,
                            status = status)
        return _item


class ShipOpManager(Manager):
    def create_operation (self, shipment, op_code):
        _op = self.create(shipment = shipment, dt = timezone.now(), op_code = op_code)
        return _op


class ItemOpManager(Manager):
    def create_operation (self, item, op_code):
        _op = self.create(item = item, dt = timezone.now(), op_code = op_code)
        return _op


class OptExtraManager(Manager):
    def create_optextra (self, shipment, quantity, unit_cost, description):
        # TODO: Write tests to verify all attributes set by managers
        _total = unit_cost * quantity
        _extra = self.create(shipment = shipment, quantity = quantity,
                             unit_cost = unit_cost, total_cost = _total,
                             description = description)
        return _extra