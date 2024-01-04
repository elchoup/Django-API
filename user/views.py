from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet


class CreateUserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
