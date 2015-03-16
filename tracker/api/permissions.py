from rest_framework import permissions
from django.contrib.auth.models import Group
from ..models import Customer


class IsOwnerOrPrivileged(permissions.BasePermission):
    """
    Only allow owners of objects to view or edit them,
    permit all members of Operator and Admin groups full access.
    """

    def has_object_permission(self, request, view, obj):
        customer_group = Group.objects.get_by_natural_key('Customer')
        operator_group = Group.objects.get_by_natural_key('Operator')
        admin_group = Group.objects.get_by_natural_key('Admin')

        if customer_group in request.user.groups.all():
            if isinstance(obj, Customer):
                return obj.user == request.user
            else:
                return obj.owner == request.user
        elif operator_group in request.user.groups or admin_group in request.user.groups:
            return True