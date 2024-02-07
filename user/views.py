from rest_framework import permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permission import IsUser


class CreateUserView(ModelViewSet):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(ModelViewSet):
    """To modify get user detail or delete only the user himself is allowed"""

    permission_classes = [IsUser]
    authentication_classes = [
        JWTAuthentication,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
