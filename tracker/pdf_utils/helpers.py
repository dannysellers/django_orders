import datetime

from reportlab.lib.styles import ParagraphStyle, StyleSheet1
# from reportlab.lib import colors
# from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, KeepTogether

from ..models import Inventory
from ..templatetags.num_filters import length


def render_footer (url, date = None):
    """
    Renders a footer used in Shipment invoice PDFs.
    :return: Paragraph
    """
    if not date:
        date = datetime.date.today().strftime("%d.%m.%Y")
        p = Paragraph('''<para>
                            {date} -
                            <a href="{url}">{url}</a> -
                            Middle Man Fulfillment
                        </para>'''.format(date = date,
                                          url = url),
                      styleSheet['Normal'])
        return p


def render_inventory (item):
    """
    Construct a Paragraph containing information about a particular Inventory obj
    :param item: Item to parse
    :type item: Inventory
    :return: Paragraph for constructing PDF
    :rtype: Paragraph
    """
    assert isinstance(item, Inventory)

    p = Paragraph(u'<para align="center">Item {}: ${}'.format(
        item.itemid,
        length(item.get_storage_fees(), 2)),
        styleSheet['Bold'])

    return KeepTogether(p)


styleSheet = StyleSheet1()
styleSheet.add(ParagraphStyle(
    name = 'Normal',
    fontSize = 10,
    leading = 12,
    # fontName = 'OpenSans',
))
styleSheet.add(ParagraphStyle(
    parent = styleSheet['Normal'],
    name = 'Small',
    fontSize = 8,
))
styleSheet.add(ParagraphStyle(
    parent = styleSheet['Normal'],
    name = 'HeaderBold',
    fontSize = 14,
    # fontName = 'OpenSans-Bold',
))
styleSheet.add(ParagraphStyle(
    parent = styleSheet['Normal'],
    name = 'Bold',
    # fontName = 'OpenSans-Bold',
))