import csv
from random import randrange, randint, random
from datetime import date, datetime
from calendar import monthrange
import os


def load_names (filename, numnames):
	print("Loading {}".format(filename))
	with open(filename, 'rU') as f:
		reader = csv.reader(f)
		first_names = reader.next()
		last_names = reader.next()

	if numnames:
		_numnames = numnames
	else:
		_numnames = 30

	# Generate a number of random pairs
	namecount = 0
	namelist = []

	while namecount < _numnames:
		i = randrange(0, len(first_names))
		j = randrange(0, len(last_names))
		namelist.append(first_names[i] + " " + last_names[j])
		namecount += 1

	print("{} customers generated.".format(len(namelist)))
	return namelist


def add_customer (name, acct, email, status):
	createdate = date(2014, randint(1, date.today().month), randint(1, date.today().day))
	c = Customer.objects.get_or_create(name = name, acct = acct, email = email,
									   status = status, createdate = createdate,
									   closedate = str(date.today()))[0]
	""" get_or_create returns (object, created)	"""
	return c


def add_item (owner, itemid, quantity, length, width, height, status):
	volume = length * width * height
	storage_fees = quantity * (float(volume) * 0.05)
	arrival = date(2014, randint(1, date.today().month), randint(1, date.today().day))
	i = Inventory.objects.get_or_create(owner = owner, itemid = itemid, quantity = quantity,
										length = length, width = width, height = height, volume = volume,
										arrival = arrival, departure = str(date.today()),
										storage_fees = storage_fees, status = status)[0]
	return i


def add_op (item, op_code):
	# TODO: make operations only occur in sequence chronologicaly?
	# Enforcing sequentiality of operations may not be necessary, as
	# in practice, they will only be created in sequence
	_month = date.today().month
	imonth = item.arrival.month
	iday = item.arrival.day

	start = datetime(2014, randint(imonth, _month),
					 randint(iday, monthrange(2014, _month)[1]), hour = randint(9, 17),
					 minute = randint(0, 59), second = randint(0, 59))

	finish = datetime(2014, randint(start.month, _month),
					  randint(start.day, monthrange(2014, _month)[1]), hour = randint(9, 17),
					  minute = randint(0, 59), second = randint(0, 59))

	""" The labor time expended isn't necessarily equal to the difference between start and
	finish datetimes, as there could be a delay in reporting. """

	labor_time = randint(1, 60)
	o = Operation.objects.get_or_create(item = item, start = start,
										finish = finish, labor_time = labor_time,
										op_code = op_code)[0]
	return o


def populate (namelist):
	customerlist = []
	for name in namelist:
		# Account number has to be unique, so roll once, check against the list, roll again
		acct = randint(10000, 99999)
		acctlist = []
		for cust in Customer.objects.all():
			acctlist.append(cust.acct)
		if acct in acctlist:
			acct = randint(10000, 99999)

		email = str(name.split(' ')[0] + "@domain.com")
		customer = add_customer(name = name, acct = acct, email = email, status = 1)
		customerlist.append(customer)
	print("{} customers added to db.".format(len(customerlist)))


def populate_items (numitems, numops):
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
							status = status, length = length, width = width, height = height)
			for j in range(status):
				add_op(item, j)
			itemcount += 1
	print("{} items added to db.".format(itemcount))


if __name__ == '__main__':
	print("Starting Customer/Inventory population script...")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracker.settings')
	from tracker.models import Customer, Inventory, Operation

	# Options
	_namelist = raw_input('CSV of names to load? (default names.csv):\t\t')
	_numnames = raw_input('Number of customers to add (default 30)?:\t')
	_numitems = raw_input('Max number of items to add per customer (default 7)?:\t')
	_numops = raw_input('Max number of operations per item (default 5)?:\t')
	# assert isinstance(_numitems, int)
	# assert isinstance(_numops, int)

	if not _namelist:
		_namelist = 'names.csv'

	_namelist = load_names(_namelist, _numnames)
	populate(_namelist)

	if not _numitems:
		_numitems = 7
	if not _numops:
		_numops = 5
	populate_items(_numitems, _numops)