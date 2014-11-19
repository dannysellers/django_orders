import os
import csv


def load_db(filename):
	with open(filename, 'r') as f:
		_reader = csv.reader(f)
		_fieldnames = _reader.next()
		if _fieldnames:
			_dictreader = csv.DictReader(f, fieldnames=_fieldnames)
			for row in _dictreader:
				name = row['Names']
				acct = row['Acct']
				add_customer(name=name, acct=acct)
		from tracker.models import Customer
		print("{} accounts loaded.".format(len(Customer.objects.all())))


def add_customer(name, acct, email='address@domain.com'):
	c = Customer.objects.get_or_create(name=name, acct=acct, email=email, status=1)
	return c


if __name__ == '__main__':
	filename = 'account_list.csv'
	print("Loading accounts from {}".format(filename))
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_tracker.settings')
	from tracker.models import Customer, Inventory
	load_db(filename)