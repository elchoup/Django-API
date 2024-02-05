from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permission import IsAuthorOrReadOnly, IsContributor, IsContributorProjects

from . import models
from user.models import User
from . import serializers


class ProjectViewSet(ModelViewSet):
    """Permission if authenticated and for all except get and create only author is authorized"""

    permission_classes = [
        IsAuthenticated,
        IsContributorProjects,
        IsAuthorOrReadOnly,
    ]
    authentication_classes = [JWTAuthentication]

    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    def get_queryset(self):
        user = self.request.user
        """ we render only projects that is contributor for """
        if self.action == "list":
            projects = user.contributor_project.all()
            return projects
        return models.Project.objects.all()

    def perform_create(self, serializer):
        """create the project with the user as author then add him to the contributors"""
        user = self.request.user
        project = serializer.save(author=user)

        models.Contributor.objects.create(user=user, project=project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContributorViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = serializers.ContributorSerializer
    queryset = models.Contributor.objects.all()

    def create(self, request):
        """Functon to create a contributor waiting for user id and project id from the user.
        Only the author of the project can create one"""
        user_id = request.data.get("user_id")
        project_id = request.data.get("project_id")

        user = get_object_or_404(User, id=user_id)
        project = get_object_or_404(models.Project, id=project_id)

        if project.author == request.user:
            if user in project.contributors.all():
                return Response(
                    {"meassage": "l'utilisateur est déjà contributeur de ce projet"}
                )
            else:
                project.contributors.add(user)
                contributor, created = models.Contributor.objects.get_or_create(
                    user=user, project=project
                )

                serializer = self.get_serializer(contributor)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    "message": "Vous n'avez pas la permission d'ajouter un contributeur à ce projet'"
                }
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            self.perform_destroy(instance)
        else:
            return Response(
                {"message": "Vous n'avez pas la permission de modifier ces données"}
            )


class IssueViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    serializer_class = serializers.IssueSerializer
    queryset = models.Issue.objects.all()

    def get_queryset(self):
        """We render only issues that user is contributor for"""
        project_id = self.kwargs.get("project_pk")
        project = get_object_or_404(models.Project, id=project_id)
        issues = models.Issue.objects.filter(project=project)
        return issues

    def create(self, request, *args, **kwargs):
        """Function to create an issue catching the id of the project in url"""
        project_id = self.kwargs.get("project_pk")
        user = self.request.user

        project = get_object_or_404(models.Project, id=project_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=user, project=project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def get_queryset(self):
        issue_id = self.kwargs.get("issue_pk")
        issue = get_object_or_404(models.Issue, id=issue_id)

        comment = models.Comment.objects.filter(issue=issue)
        return comment

    def create(self, request, *args, **kwargs):
        """Function to create a comment catching the id of the issue in the url"""
        issue_id = self.kwargs.get("issue_pk")
        user = self.request.user

        issue = get_object_or_404(models.Issue, id=issue_id)
        project = issue.project
        print(project.contributors)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=user, issue=issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
