import os
import csv


def fix_date(datestr):
	"""
	Dates in the account_list are MM/DD/YYYY, but Django's DateField
	requires YYYY-MM-DD format
	"""
	_createdate = datestr.split('/')
	if len(_createdate[2]) == 2:
		_createdate[2] = '20' + str(_createdate[2])
	_createdate = [_createdate[2], _createdate[0], _createdate[1]]
	_createdate = '-'.join(_createdate)
	return _createdate


def load_db (filename):
	with open(filename, 'rU') as f:
		_reader = csv.reader(f)
		_fieldnames = _reader.next()
		if _fieldnames:
			_dictreader = csv.DictReader(f, fieldnames = _fieldnames)
			_dictreader.next()  # don't parse the first row again
			for row in _dictreader:
				name = row['Names']
				acct = row['Acct']
				createdate = fix_date(row['Date Created'])
				add_customer(name=name, acct=acct, createdate=createdate)
			# print("{} accounts loaded.".format(len(Customer.objects.all())))


def add_customer (name, acct, createdate, email='address@domain.com'):
	c = Customer.objects.get_or_create(name = name, acct = acct, email = email,
									   status = 1, createdate = createdate)
	return c


if __name__ == '__main__':
	filename = 'account_list.csv'
	print("Loading accounts from {}".format(filename))
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracker.settings')
	from tracker.models import Customer
	load_db(filename)