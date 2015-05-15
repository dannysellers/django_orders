from django import template

register = template.Library()


@register.filter
def length (value, length=2):
    """
    Truncates `value` to `length`
    :type value: float
    :type length: int
    :rtype: str
    """
    if value:
        _length = int(length)
        _string = str(value).split('.')
        if len(_string[1]) == 1:
            _string[1] += '0' * _length - 1
        return _string[0] + '.' + _string[1][:_length]
    else:
        return '0.{}'.format('0' * int(length))



@register.filter
def storage_fee_total (item_list, stored = True):
    """
    Sums the storage fees of a given item list
    :param item_list: List of items to process
    :param stored: Whether to consider only items still in storage (default True)
    :return: Storage fee sum
    """
    _sum = float(0)
    for item in item_list:
        if stored:
            if item.status != '4':
                _sum += item.storage_fees
        else:
            _sum += item.storage_fees
    return length(_sum, 2)


@register.filter
def stored_count (unit_list):
    """
    Returns count of items (Inventory or Shipment) that are still in storage (status < 4)
    :param unit_list: Set of items to filter
    :type unit_list: QuerySet
    :return: Number of shipments with status < 4
    :rtype: Int
    """
    _count = int(0)
    for unit in unit_list:
        if int(unit.status) < 4:
            _count += 1
    return _count
