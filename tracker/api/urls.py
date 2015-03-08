from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'customers', views.CustomerViewSet)
# router.register(r'shipments', views.ShipmentViewSet)
router.register(r'inventory', views.InventoryViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^shipments/$', views.shipment_list),
    url(r'^shipments/$', views.ShipmentList.as_view()),
    # url(r'^shipments/(?P<pk>[0-9]+)$', views.shipment_detail),
    url(r'^shipments/(?P<pk>[0-9]+)$', views.ShipmentDetail.as_view()),
]

# Incompatible with router urls, which accomplishes the same task for routed viewsets
urlpatterns = format_suffix_patterns(urlpatterns)