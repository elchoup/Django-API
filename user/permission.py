from rest_framework import permissions
from .models import User


class IsUser(permissions.BasePermission):
    """Permission to make sure only the user can modify his informations or delete his account"""

    message = "Vous ne pouvez accéder, modifier ou supprimer seulement le compte vous appartenant"

    def has_object_permission(self, request, view, obj):
        if view.action in ["retrieve", "update", "partial_update", "destroy"]:
            return request.user == obj
