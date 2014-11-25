import os
import csv
from random import randrange, randint
from datetime import date


def load_names(filename):
	with open(filename, 'rU') as f:
		reader = csv.reader(f)
		first_names = reader.next()
		last_names = reader.next()

	# Generate a number of random pairs
	namecount = 0
	namelist = []

	while namecount < 30:
		i = randrange(0, len(first_names))
		j = randrange(0, len(last_names))
		namelist.append(first_names[i] + " " + last_names[j])
		namecount += 1

	return namelist


def add_customer(name, acct, email, status):
	c = Customer.objects.get_or_create(name=name, acct=acct, email=email,
									   status=status, createdate=str(date.today()),
									   closedate=str(date.today()))[0]
	""" get_or_create returns (object, created)	"""
	return c


def add_item(owner, itemid, quantity, weight):
	storage_fees = quantity * weight
	i = Inventory.objects.get_or_create(owner=owner, itemid=itemid, quantity=quantity,
										weight=weight, arrival=str(date.today()),
										departure=str(date.today()), storage_fees=storage_fees)[0]
	return i


def add_op(item, start, finish):
	o = Operation.objects.get_or_create(item=item, start=start, finish=finish)[0]
	return o


def populate(namelist):
	customerlist = []
	for name in namelist:
		acct = randint(10000, 99999)
		email = str(name.split(' ')[0] + "@domain.com")
		customer = add_customer(name=name, acct=acct, email=email, status=1)
		customerlist.append(customer)

		itemid = len(Inventory.objects.all())  # itemid has to be unique, so we just iterate at creation
		for i in range(randint(0, 3)):  # number of separate items to add per customer
			quantity = randint(0, 10)
			weight = randint(0, 50)
			itemid += 1
			item = add_item(owner=customer, itemid=itemid, quantity=quantity, weight=weight)
			add_op(item, str(date.today()), str(date.today()))


if __name__ == '__main__':
	print("Starting Customer/Inventory population script...")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracker.settings')
	from tracker.models import Customer, Inventory, Operation
	_namelist = load_names('names.csv')
	populate(_namelist)