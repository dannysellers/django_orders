import csv
from random import randrange, randint, random
from datetime import date, datetime
from calendar import monthrange

import os


############################
#### Globals / defaults ####
############################
td = date.today()
DEFAULT_CUSTOMER_NUMBER = 15
DEFAULT_ITEM_NUMBER = 7
DEFAULT_NAMELIST = 'names.csv'


def rand_date ():
	_year = td.year
	_month = randint(1, 12)
	_day = randint(1, monthrange(_year, _month)[1])
	return date(_year, _month, _day)


def load_names (filename, numnames):
	print("Loading {}".format(filename))
	with open(filename, 'rU') as f:
		reader = csv.reader(f)
		first_names = reader.next()
		last_names = reader.next()

	# Generate a number of random pairs
	namecount = 0
	namelist = []

	while namecount < int(numnames):
		i = randrange(0, len(first_names))
		j = randrange(0, len(last_names))
		namelist.append(first_names[i] + " " + last_names[j])
		namecount += 1

	print("{} customers generated.".format(len(namelist)))
	return namelist


def add_customer (name, acct, email, status):
	createdate = rand_date()
	c = Customer.objects.get_or_create(name = name, acct = acct, email = email,
									   status = status, createdate = createdate,
									   closedate = td)[0]
	""" get_or_create returns (object, created)	"""
	return c


def add_item (owner, itemid, quantity, length, width, height, status):
	volume = length * width * height
	storage_fees = quantity * (float(volume) * 0.05)

	arrival = rand_date()
	i = Inventory.objects.get_or_create(owner = owner, itemid = itemid, quantity = quantity,
										length = length, width = width, height = height, volume = volume,
										arrival = arrival, departure = td,
										storage_fees = storage_fees, status = status)[0]
	return i


def add_op (item, op_code, user):
	# Enforcing sequentiality of operations may not be necessary, as
	# in practice, they will only be created in sequence
	imonth = item.arrival.month
	iday = item.arrival.day

	dt = datetime(year = td.year, month = randint(imonth, td.month),
				  day = randint(iday, monthrange(td.year, td.month)[1]),
				  hour = randint(9, 17), minute = randint(0, 59), second = randint(0, 59))

	o = Operation.objects.get_or_create(item = item, dt = dt,
										op_code = op_code, user = user)[0]
	return o


def add_shipment (item, user):
	imonth = item.arrival.month
	iday = item.arrival.day

	start = datetime(year = td.year, month = randint(imonth, td.month),
					 day = randint(iday, monthrange(td.year, td.month)[1]),
					 hour = randint(9, 17), minute = randint(0, 59), second = randint(0, 59))

	finish = datetime(year = td.year, month = randint(imonth, td.month),
					  day = randint(iday, monthrange(td.year, td.month)[1]),
					  hour = randint(9, 17), minute = randint(0, 59), second = randint(0, 59))

	labor_time = randint(0, 120)

	s = Shipment.objects.get_or_create(item = item, user = user, start = start,
									   finish = finish, labor_time = labor_time)[0]
	add_opt_extras(s)

	return s


def add_opt_extras (shipment):
	quantity = randint(0, 5)
	unit_cost = random() * randint(0, 10)
	description = "Fake item x {}".format(quantity)

	op = OptExtras.objects.get_or_create(shipment = shipment, quantity = quantity,
										 unit_cost = unit_cost, description = description)[0]

	return op


def populate (namelist):
	customerlist = []
	for name in namelist:
		# Account number has to be unique, so roll once, check against the list, roll again
		acct = randint(10000, 99999)
		acctlist = []
		for cust in Customer.objects.all():
			acctlist.append(cust.acct)
		if acct in acctlist:  # roll again
			acct = randint(10000, 99999)

		email = str(name.split(' ')[0] + "@domain.com")
		customer = add_customer(name = name, acct = acct, email = email, status = 1)
		customerlist.append(customer)
	print("{} customers added to db.".format(len(customerlist)))


def populate_items (numitems, user):
	customerlist = Customer.objects.all()
	if not customerlist:
		_namelist = raw_input('No customers found. Add how many?:\t')
		populate(_namelist)

	itemid = len(Inventory.objects.all())  # itemid has to be unique, so just iterate at creation
	itemcount = 0
	for customer in customerlist:
		for i in range(randint(1, int(numitems))):
			quantity = randint(1, 10) + random()  # random gives decimal [0.0, 1.0)
			length = (randint(1, 36) + random()) / 12  # storage fees are in ft^3
			width = (randint(1, 36) + random()) / 12
			height = (randint(1, 36) + random()) / 12
			itemid += 1
			status = randint(0, 4)
			item = add_item(owner = customer, itemid = itemid, quantity = quantity,
							status = status, length = length, width = width,
							height = height)
			for j in range(status + 1):
				add_op(item, j, user)
			add_shipment(i, user)
			itemcount += 1
	print("{} items added to db.".format(itemcount))


if __name__ == '__main__':
	print("Starting Customer/Inventory population script...")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracker.settings')
	from tracker.models import Customer, Inventory, Operation, Shipment, OptExtras
	from django.contrib.auth.models import User

	u = User.objects.all()[0]

	# Options
	_namelist = raw_input('CSV of names to load? (default names.csv):  ')
	_numnames = raw_input('Number of customers to add (default {0})?:  '.format(DEFAULT_CUSTOMER_NUMBER))
	_numitems = raw_input('Max number of items to add per customer (default {0})?:  '.format(DEFAULT_ITEM_NUMBER))

	if not _namelist:
		_namelist = DEFAULT_NAMELIST
	if not _numnames:
		_numnames = DEFAULT_CUSTOMER_NUMBER
	if not _numitems:
		_numitems = DEFAULT_ITEM_NUMBER

	_namelist = load_names(_namelist, _numnames)
	populate(_namelist)
	populate_items(_numitems, u)