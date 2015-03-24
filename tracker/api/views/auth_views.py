from datetime import datetime, timedelta
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.http import HttpResponse
import json


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post (self, request):
        serializer = self.serializer_class(data = request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user = serializer.object['user'])

        utc_now = datetime.utcnow()
        if not created and token.created < utc_now - timedelta(hours = 48):
            token.delete()
            token = Token.objects.create(user = serializer.object['user'])
            token.created = datetime.utcnow()
            token.save()

            response_data = {'token': token.key}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)