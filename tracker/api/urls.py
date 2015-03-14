from django.conf.urls import url, include
# from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from views import detail_views, list_views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^users/$', list_views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', detail_views.UserDetail.as_view()),
    url(r'^shipments/$', list_views.ShipmentList.as_view()),
    url(r'^shipments/(?P<shipid>[0-9]+)/$', detail_views.ShipmentDetail.as_view()),
    url(r'^customers/$', list_views.CustomerList.as_view()),
    url(r'^customers/(?P<acct>[0-9]+)/$', detail_views.CustomerDetail.as_view()),
    url(r'^inventory/$', list_views.InventoryList.as_view()),
    url(r'^inventory/(?P<itemid>[0-9]+)/$', detail_views.InventoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)