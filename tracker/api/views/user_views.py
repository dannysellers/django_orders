from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer
from ..permissions import IsOwnerOrPrivileged, IsOwnerOrPrivilegedObject


class UserList(APIView):
    permission_classes = (IsOwnerOrPrivileged,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get (self, request, format = None):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True, context = {'request': request})
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve or update a User instance. Users cannot be destroyed or
    deactivated via the API, and must be removed by an Operator or Admin.
    """
    permission_classes = (IsOwnerOrPrivilegedObject,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @staticmethod
    def get_object (pk):
        try:
            return User.objects.get(id = pk)
        except User.DoesNotExist:
            raise Http404

    def get (self, request, pk, format = None):
        user = self.get_object(pk)
        # serializer = UserSerializer(user)
        serializer = UserSerializer(user,
                                    context = {'request': request})
        return Response(serializer.data)

    def put (self, request, pk, format = None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)