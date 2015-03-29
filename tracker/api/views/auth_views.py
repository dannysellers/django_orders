# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework import exceptions

from rest_auth.views import Login

from ..serializers import CustomTokenSerializer
# from ..authentication import ExpiringTokenAuthentication

# from datetime import datetime, timedelta

# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# import json
# from datetime import datetime, timedelta


class CustomTokenLogin(Login):
    """
    Overridden rest_auth.view.login to use CustomTokenSerializer
    """
    response_serializer = CustomTokenSerializer


# class ObtainExpiringAuthToken(ObtainAuthToken):
# # serializer_class = ExpiringAuthTokenSerializer
#     serializer_class = AuthTokenSerializer
#
#     def post (self, request):
#         serializer = self.serializer_class(data = request.DATA)
#         # serializer = AuthTokenSerializer(data = request.DATA)
#         serializer.is_valid(raise_exception = True)
#
#         token, created = Token.objects.get_or_create(user = serializer.object['user'])
#
#         utc_now = datetime.utcnow()
#         if not created and token.created < utc_now - timedelta(hours = 48):
#             token.delete()
#             token = Token.objects.create(user = serializer.object['user'])
#             token.created = datetime.utcnow()
#             token.save()
#
#             response_data = {'token': token.key}
#             return HttpResponse(json.dumps(response_data), content_type='application/json')
#
#         # return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# class ExpiringAuthTokenLogin(Login):
#     @csrf_exempt
#     def login (self):
#         self.user = self.serializer.validated_data['user']
#         self.token, created = self.token_model.objects.get_or_create(
#             user = self.user
#         )
#
#         utc_now = datetime.utcnow()
#         if not created and self.token.created < utc_now - timedelta(hours = 48):
#             raise exceptions.AuthenticationFailed(
#                 'Token has expired. Log in with your username and password to generate a new token.')
#
#     @csrf_exempt
#     def post (self, request, *args, **kwargs):
#         self.serializer = self.get_serializer(data = self.request.DATA)
#         if not self.serializer.is_valid():
#             return self.get_error_response()
#         self.login()
#         return self.get_response()