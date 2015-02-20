from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
# import views
# import acct_views
# import inv_views
# import ship_views
# import report_views

# General / report patterns
urlpatterns = patterns('tracker.views',
   url(r'^$', 'index'),
   url(r'^register/$', 'register'),
   url(r'^login/$', 'user_login', name='login'),
   url(r'^logout/$', 'user_logout', name='logout'),
)

# Account patterns
urlpatterns += patterns('tracker.acct_views',
	url(r'^accounts$', 'accounts'),
	url(r'^accounts/(?P<account_url>\d+)/$', 'account_page'),
	url(r'^add_account/$', 'add_account'),
	url(r'^acct_info$', 'acct_info'),
)

# Inventory patterns
urlpatterns += patterns('tracker.inv_views',
	url(r'^inventory$', 'inventory'),
	# url(r'^accounts/(?P<account_url>\S+)/add_inventory/$', 'add_item'),
	# url(r'^add_inventory/$', 'add_item', name='add_inventory'),
	url(r'^manage_items$', 'change_item_status', name='change_item_status'),
)

# Shipment patterns
urlpatterns += patterns('tracker.ship_views',
	url(r'^shipment$', 'shipment'),
	url(r'^ship_info$', 'ship_info'),
	url(r'^ship_extras$', 'ship_extras'),
	url(r'^accounts/(?P<account_url>\S+)/add_shipment/$', 'add_shipment'),
)

# Report patterns
urlpatterns += patterns('tracker.report_views',
	url(r'^shipreport/(?P<shipid>\d+)$', 'shipment_report'),
	url(r'^reports/$', 'reports'),
	url(r'^shipment_ajax$', 'ajax_graph'),
	url(r'^ajax2$', 'stored_volume_over_time'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # for deployment purposes