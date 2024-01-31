from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Project


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Function to verificate if user is author of one project"""

    message = "Vous devez être auteur pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True

        if view.action in ["update", "partial_update", "destroy"]:
            return request.user == obj.author

        return False


class IsContributor(permissions.BasePermission):
    """Function permission to verificate if user is contributors of one project"""

    message = "Vous n'êtes pas contributeur de ce projet"

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        print(project_id)
        project = get_object_or_404(Project, id=project_id)

        return request.user in project.contributors.all()


class IsContributorProjects(permissions.BasePermission):
    """Function permission to verificate if user is contributors of projects"""

    message = "Vous n'êtes contributeur d'aucun projet"

    def has_permission(self, request, view):
        projects = Project.objects.filter(contributors=request.user)
        if projects.exists():
            return True
        if view.action == "create":
            return True
        if view.action in ["update", "partial_update", "destroy"]:
            return True
