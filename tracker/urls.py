from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^about/$', views.about, name='about'),
   url(r'^inventory/$', views.inventory, name='inventory'),
   url(r'^accounts/(?P<account_name_url>\S+)/add_item/$', views.add_item, name='add_item'),
)

# Account patterns
urlpatterns += patterns('',
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/(?P<bool_active>\w+)/$', views.accounts, name='accounts'),
    url(r'^accounts/(?P<account_url>)(\w+|\d{5})/$', views.account_page, name='account_page'),
    url(r'^add_account$', views.add_account, name='add_account'),
    url(r'^accounts/(?P<account_num_url>\d+)/remove_account$', views.remove_account,
        name = 'remove_account'),
)

# Inventory patterns