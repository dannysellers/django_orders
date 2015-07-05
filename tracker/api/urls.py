from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from views import customer_views, inventory_views, \
    shipment_views, user_views, auth_views, contact_view, \
    workorder_views

urlpatterns = [
    url(r'^users/(?P<pk>[0-9]+)/$', user_views.UserDetail.as_view(), name = 'user_detail'),
    # url(r'^shipments/$', shipment_views.ShipmentList.as_view(), name = 'shipment_list'),
    # url(r'^shipments/(?P<shipid>[0-9]+)/$', shipment_views.ShipmentDetail.as_view(), name = 'shipment_detail'),
    # url(r'^customers/$', customer_views.CustomerList.as_view(), name = 'customer_list'),
    url(r'^customers/(?P<acct>[0-9]+)/$', customer_views.CustomerDetail.as_view(), name = 'customer_detail'),
    # url(r'^inventory/$', inventory_views.InventoryList.as_view(), name = 'inventory_list'),
    # url(r'^inventory/(?P<itemid>[0-9]+)/$', inventory_views.InventoryDetail.as_view(), name = 'inventory_detail'),
    url(r'^submitorder/(?P<acct>[0-9]+)/$', user_views.receive_work_order, name = 'submit_order'),
    # url(r'^invoice/(?P<shipid>[0-9]+)/$', shipment_views.shipment_report, name = 'invoice'),
    # url(r'^invoice/(?P<shipid>[0-9]+)/$', shipment_views.ShipmentInvoice.as_view(), name = 'invoice'),
    url(r'^workorders/(?P<id>[0-9])+/$', workorder_views.WorkOrderDetail.as_view()),
    url(r'^workorders/$', workorder_views.WorkOrderList.as_view(), name = 'workorder_list'),
    url(r'^contact/$', contact_view.contact_us, name = 'contact_us'),
    url(r'^auth/login/$', auth_views.CustomTokenLogin.as_view(), name = 'login'),
    url(r'^auth/', include('rest_auth.urls'))  # This URL regex can't be terminated, so rest_auth.urls can take over
]

urlpatterns = format_suffix_patterns(urlpatterns)
