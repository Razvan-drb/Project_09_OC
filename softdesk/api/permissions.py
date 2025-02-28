from rest_framework import permissions

from api.models import Contributor


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour autoriser uniquement l'auteur d'un objet à le modifier ou le supprimer.
    """

    def has_object_permission(self, request, view, obj):
        # Lire les données est autorisé pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Seul l'auteur de l'objet peut le modifier ou le supprimer
        return obj.author == request.user


class IsProjectContributor(permissions.BasePermission):
    """
    Permission qui vérifie si l'utilisateur est contributeur du projet.
    """

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj.issue.project, user=request.user).exists() or obj.author == request.user


class IsCommentAuthor(permissions.BasePermission):
    """
    Seul l'auteur d'un commentaire peut le modifier ou le supprimer.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
