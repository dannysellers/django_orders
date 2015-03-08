from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from api import urls as api_urls

# Index
urlpatterns = patterns('tracker.views.misc_views',
   url(r'^$', 'index'),
)

# Authentication patterns
urlpatterns += patterns('tracker.views.auth_views',
    url(r'^register/$', 'register'),
    url(r'^login/$', 'user_login', name = 'login'),
    url(r'^logout/$', 'user_logout', name = 'logout'),
)

# Account patterns
urlpatterns += patterns('tracker.views.acct_views',
    url(r'^accounts$', 'accounts'),
    url(r'^accounts/(?P<account_url>\d+)/$', 'account_page'),
    url(r'^add_account/$', 'add_account'),
    url(r'^acct_info$', 'acct_info'),
)

# Inventory patterns
urlpatterns += patterns('tracker.views.inv_views',
    url(r'^inventory$', 'inventory'),
    # url(r'^accounts/(?P<account_url>\S+)/add_inventory/$', 'add_item'),
    # url(r'^add_inventory/$', 'add_item', name='add_inventory'),
    url(r'^manage_items$', 'change_item_status', name = 'change_item_status'),
)

# Shipment patterns
urlpatterns += patterns('tracker.views.ship_views',
    url(r'^shipment$', 'shipment'),
    url(r'^ship_info$', 'ship_info'),
    url(r'^ship_extras$', 'ship_extras'),
    url(r'^accounts/(?P<account_url>\S+)/add_shipment/$', 'add_shipment'),
)

# Report patterns
urlpatterns += patterns('tracker.views.report_views',
    url(r'^shipreport/(?P<shipid>\d+)$', 'shipment_report'),
    url(r'^reports/$', 'reports'),
    url(r'^query_ajax$', 'ajax'),
    url(r'^form_ajax/(?P<model_name>\w+)$', 'form_ajax'),
)

# API patterns
urlpatterns += patterns('',
    url(r'^api/', include(api_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

# For deployment
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)