from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^about/$', views.about, name='about'),
   url(r'^accounts/$', views.accounts, name='accounts'),  # account list
   url(r'^accounts/(?P<account_name_url>\S+)/$', views.account_page, name='account_page'),  # individual acct
   url(r'^add_account/$', views.add_account, name='add_account'),
   url(r'^accounts/(?P<account_name_url>\S+)/remove_account$', views.remove_account, name='remove_account'),
   url(r'^inventory/$', views.inventory, name='inventory'),
   url(r'^accounts/(?P<account_name_url>\S+)/add_item/$', views.add_item, name='add_item'),
)