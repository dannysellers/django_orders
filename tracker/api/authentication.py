from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from datetime import timedelta, datetime


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Authentication class for ExpiringToken
    """

    def authenticate_credentials (self, key):
        try:
            token = self.model.objects.get(key = key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.customer.is_active():
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.utcnow()

        if token.created < utc_now - timedelta(hours = 48):
            raise exceptions.AuthenticationFailed('Token has expired')

        return tuple(token.user, token)