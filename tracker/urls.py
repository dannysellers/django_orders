from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from api import urls as api_urls

# Index
urlpatterns = patterns('tracker.views.misc_views',
   url(r'^$', 'index', name = 'index'),
   url(r'^workorders/$', 'work_orders', name = 'work_order_list'),
   url(r'^workorders/(?P<id>\d+)/$', 'work_order_detail', name = 'work_order_detail'),
   url(r'^submitorder/$', 'submit_work_order', name = 'submit_work_order'),
)

# Authentication patterns
urlpatterns += patterns('tracker.views.auth_views',
    url(r'^register/$', 'register', name = 'register'),
    url(r'^login/$', 'user_login', name = 'login'),
    url(r'^logout/$', 'user_logout', name = 'logout'),
)

# Account patterns
urlpatterns += patterns('tracker.views.acct_views',
    url(r'^accounts$', 'accounts', name = 'account_list'),
    url(r'^accounts/(?P<account_id>\d+)/$', 'account_page', name = 'account_detail'),
    url(r'^add_account/$', 'add_account', name = 'add_account'),
    url(r'^acct_info$', 'acct_info', name = 'account_info'),
)

# Inventory patterns
urlpatterns += patterns('tracker.views.inv_views',
    url(r'^inventory$', 'inventory', name = 'inventory_detail'),
    # url(r'^accounts/(?P<account_url>\S+)/add_inventory/$', 'add_item'),
    # url(r'^add_inventory/$', 'add_item', name='add_inventory'),
    url(r'^manage_items$', 'change_item_status', name = 'change_item_status'),
)

# Shipment patterns
urlpatterns += patterns('tracker.views.ship_views',
    url(r'^shipment/(?P<shipid>\d+)$', 'shipment', name = 'shipment_detail'),
    url(r'^ship_info$', 'ship_info', name = 'ship_info'),
    url(r'^ship_extras$', 'ship_extras', name = 'ship_extras'),
    url(r'^accounts/(?P<account_url>\S+)/add_shipment/$', 'add_shipment', name = 'add_shipment'),
)

# Report patterns
urlpatterns += patterns('tracker.views.report_views',
    url(r'^reports/$', 'reports', name = 'reports'),
    url(r'^query_ajax$', 'graph_query', name = 'graph_query'),
    url(r'^form_ajax/(?P<model_name>\w+)$', 'form_ajax', name = 'form_ajax'),
)

# Invoice patterns
urlpatterns += patterns('tracker.views.invoice_views',
    url(r'^shipreport/(?P<shipid>\d+)$', 'shipment_report', name = 'shipment_report'),
    # url(r'^template/(?P<shipid>\d+)$', 'invoice_template', name = 'invoice_template'),
)

# API patterns
urlpatterns += patterns('',
    url(r'^api/', include(api_urls)),
)

# For deployment
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)