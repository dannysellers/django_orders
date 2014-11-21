from django.conf.urls import patterns, url
import views
import acct_views
import inv_views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^about/$', views.about, name='about'),
)

# Account patterns
urlpatterns += patterns('',
    url(r'^accounts/$', acct_views.accounts, name='accounts'),
    url(r'^accounts/(?P<bool_active>\w+)/$',acct_views.accounts, name='accounts'),
    url(r'^accounts/(?P<account_url>)(\w+|\d{5})/$',acct_views.account_page, name='account_page'),
    url(r'^add_account/$',acct_views.add_account, name='add_account'),
    url(r'^accounts/(?P<account_num_url>\d+)/remove_account$',acct_views.remove_account,
        name = 'remove_account'),
)

# Inventory patterns
urlpatterns += patterns('',
    url(r'^inventory/$', inv_views.inventory, name='inventory'),
    url(r'^accounts/(?P<account_name_url>\S+)/add_item/$', inv_views.add_item, name = 'add_item'),
    url(r'^accounts/(?P<account_name_url>\S+)/add_inventory/$', inv_views.add_item,
        name='add_item'),
)