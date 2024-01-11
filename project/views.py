from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404

from . import models
from . import serializers

# Create your views here.
"""var jsonData = pm.response.json();
pm.environment.set("token", jsonData.access);"""


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)

        contributor, created = models.Contributor.objects.get_or_create(user=user)
        project.contributors.add(contributor)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Vous n'avez pas la permission de modifier ces données"}
            )
