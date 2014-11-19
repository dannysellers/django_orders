from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
					   url(r'^$', views.index, name='index'),
					   url(r'^about/$', views.about, name='about'),
					   url(r'^accounts/$', views.accounts, name='accounts'),
					   url(r'^accounts/(?P<account_name_url>\w+)/$', views.accountpage, name='account_page'),
					   url(r'^add_account/$', views.add_account, name='add_account'),
					   url(r'^accounts/(?P<account_name_url>\w+)/add_item/$', views.add_item, name='add_item'),
					   url(r'^inventory/$', views.inventory, name='inventory'),
)