# from models import Customer, Inventory
# import utils
# import json
# from datetime import date, datetime


# clist = Customer.objects.all()
# ilist = Inventory.objects.all()

"""

json(customer) = {
	'name': 'Bob Smith',
	'acct': 12345,
	'email': 'bob@domain.com',
	'status': 1,
	'createdate': createdate,
	'closedate': createdate
}

json(inventory) = {
	'owner': foreignkey(customer),
	'itemid': itemid,
	'quantity': 1,
	'length': 1.00,
	'width': 1.00,
	'height': 1.00,
	'volume': 1.00,
	'palletized': False,
	'arrival': arrival,
	'departure': arrival,
	'status': 1,
	'storage_fees': 0.05,
	'status_history':
		[{
			'datetime': datetime,
			'code': 0,
			'user': user
		},
		{
			'datetime': datetime,
			'code': 1,
			'user': user
		}]
}

json(shipment) = {
	'item': foreignkey(item),
	'start': datetime,
	'finish': datetime,
	'labor_time': labor_time,
	'optionals':
		{
			'stickers': 0,
			'stickers_labor': 0,
			'reboxing': 0,
			'reboxing_labor': 0,
			'damage_inspection': 0,
			'damage_inspection_labor': 0,
			'labeling': 0,
			'labeling_labor': 0
		}
	'addl_charges':
		[{
			'quantity': 1,
			'description': 'packing tape roll',
			'unit_cost': 3.50
		},
		{
			'quantity': 2,
			'description': 'plastic bag',
			'unit_cost': 1.00
		}]
}

"""