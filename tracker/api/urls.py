from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'shipments', views.ShipmentViewSet)
router.register(r'inventory', views.InventoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]