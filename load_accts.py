import os
import csv

"""
This script is largely specific to my account_list, which has Excel-formatted date codes
and Customer and Business names comma-separated within the same cell

For a general csv, remove fix_date call from line ## and fix_cust_names from line ##
"""


def fix_date(datestr):
	"""
	Dates in the account_list are MM/DD/YYYY, but Django's DateField
	requires YYYY-MM-DD format
	"""
	_createdate = datestr.split('/')
	_createdate = [_createdate[2], _createdate[0], _createdate[1]]
	_createdate = '-'.join(_createdate)
	return _createdate


def fix_cust_names(namestr):
	"""
	Some customers have "Business, FirstName LastName" as their 'Names' field.
	Rather than trying to allow punctuation in URLs, I've split those up into
	distinct model attributes
	"""
	if ',' in namestr:
		namelist = namestr.split(', ')
		# bizname = namelist[0]
		# custname = namelist[1]
		# return [custname, bizname]
		return namelist
	else:
		return namestr


def load_db (filename):
	with open(filename, 'r') as f:
		_reader = csv.reader(f)
		_fieldnames = _reader.next()
		if _fieldnames:
			_dictreader = csv.DictReader(f, fieldnames = _fieldnames)
			_dictreader.next()  # don't parse the first row again
			for row in _dictreader:
				namelist = fix_cust_names(row['Names'])
				name = namelist[1]
				if len(namelist) == 2:
					bizname = namelist[0]
				else:
					bizname = 'N/A'
				acct = row['Acct']
				createdate = fix_date(row['Date Created'])
				add_customer(name=name, bizname=bizname, acct=acct, createdate=createdate)
			print("{} accounts loaded.".format(len(Customer.objects.all())))


def add_customer (name, bizname, acct, createdate, email='address@domain.com'):
	c = Customer.objects.get_or_create(name = name, bizname = bizname, acct = acct,
									   email = email, status = 1, createdate = createdate)
	return c


if __name__ == '__main__':
	filename = 'account_list.csv'
	print("Loading accounts from {}".format(filename))
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracker.settings')
	from tracker.models import Customer
	load_db(filename)