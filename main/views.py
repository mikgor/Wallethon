from abc import ABC
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from knox.views import LoginView as KnoxLoginView
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from apps.permissions.mixins import PermissionViewSetMixin
from main.models import User
from main.serializers.serializers import UserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        data = super().get_post_response_data(request, token, instance)
        data['user'] = request.user.uuid
        return data


class ProtectedModelViewSet(PermissionViewSetMixin, ModelViewSet, ABC):
    http_method_names = ['get', 'head', 'post', 'put', 'patch', 'delete']


class UserViewSet(ProtectedModelViewSet):
    model = User
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return User.objects.none()
        return self.model.objects.all()

