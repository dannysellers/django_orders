from datetime import timedelta

from models import Shipment
from templatetags.num_filters import length
from django.utils import timezone


def get_shipment_cost (shipid):
	"""
	Tallies up all costs associated with a particular shipment. Factors include:
	--Labor time: Billed at $35 per hour
	--Storage fees: Per item, $0.05 per lb per day after the first 7 days
	--Optional Extras: additional services or resources
	:param shipid: Shipment ID
	:type shipid: int
	:return: Cost string
	:rtype: str
	"""
	shipment = Shipment.objects.get(shipid = shipid)
	items = shipment.inventory_set.all()
	labor = shipment.labor_time
	extras = shipment.optextras_set.all()

	cost = 0.00
	# TODO: Make cost settings more easily configurable
	cost += 35 * (labor / float(60))  # labor = $35.00/hr, measured in mins
	for item in items:
		daily_fees = item.get_storage_fees()
		time_in_storage = timezone.now().date() - item.arrival
		billable_storage = time_in_storage - timedelta(days = 7)
		cost += daily_fees * billable_storage.days
	for extra in extras:
		cost += extra.total_cost

	cost = length(cost, 2)

	return cost