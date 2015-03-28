from django.conf.urls import url, include
# from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from views import customer_views, inventory_views, \
    shipment_views, user_views, auth_views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^users/$', user_views.UserList.as_view(), name = 'user_list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_views.UserDetail.as_view(), name = 'user_detail'),
    url(r'^shipments/$', shipment_views.ShipmentList.as_view(), name = 'shipment_list'),
    url(r'^shipments/(?P<shipid>[0-9]+)/$', shipment_views.ShipmentDetail.as_view(), name = 'shipment_detail'),
    url(r'^customers/$', customer_views.CustomerList.as_view(), name = 'customer_list'),
    url(r'^customers/(?P<acct>[0-9]+)/$', customer_views.CustomerDetail.as_view(), name = 'customer_detail'),
    url(r'^inventory/$', inventory_views.InventoryList.as_view(), name = 'inventory_list'),
    url(r'^inventory/(?P<itemid>[0-9]+)/$', inventory_views.InventoryDetail.as_view(), name = 'inventory_detail'),
    url(r'^auth/login/$', auth_views.Login.as_view(), name = 'login'),
    url(r'^auth/', include('rest_auth.urls'))  # This URL regex can't be terminated, so rest_auth.urls can take over
]

urlpatterns = format_suffix_patterns(urlpatterns)