from django.conf.urls import patterns, url
import views
import acct_views
import inv_views

# General / report patterns
urlpatterns = patterns('',
   url(r'^$', views.index, name = 'index'),
   url(r'^about/$', views.about, name = 'about'),
   url(r'^register/$', views.register, name='register'),
   url(r'^login/$', views.user_login, name='login'),
   url(r'^logout/$', views.user_logout, name='logout'),
)

# Account patterns
urlpatterns += patterns('',
	url(r'^accounts$', acct_views.accounts, name = 'accounts'),
	url(r'^accounts/(?P<account_url>\d+)/$', acct_views.account_page, name = 'account_page'),
	url(r'^add_account/$', acct_views.add_account, name = 'add_account'),
	url(r'^acct_info', acct_views.acct_info, name = 'acct_info'),
)

# Inventory patterns
urlpatterns += patterns('',
	url(r'^inventory', inv_views.inventory, name = 'inventory'),
	url(r'^accounts/(?P<account_url>\S+)/add_inventory/$', inv_views.add_item, name = 'add_item'),
	url(r'^add_inventory/$', inv_views.add_item, name='add_inventory'),
	url(r'^manage_items/$', inv_views.change_item_status, name='manage_items'),
	url(r'^change_status', inv_views.change_item_status, name='change_status'),  # change one item's status
	# url(r'^item_status_ajax/(?P<item_id>\w+/$)', inv_views.item_status_ajax, name='status_ajax'),
)

# Shipment patterns
urlpatterns += patterns('',
	url(r'^shipment', inv_views.shipment, name='shipment'),
	url(r'^ship_info', inv_views.ship_info, name='ship_info'),  # for POSTing shipment info
)