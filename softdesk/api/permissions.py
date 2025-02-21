from rest_framework import permissions

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
