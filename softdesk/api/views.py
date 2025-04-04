from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly, IsProjectContributor, IsCommentAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

# class ContributorViewSet(viewsets.ModelViewSet):
#     queryset = Contributor.objects.all()
#     serializer_class = ContributorSerializer
#     permission_classes = [IsAuthenticated]

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()
        if contributor.project.author != request.user:
            raise PermissionDenied("Seul l'auteur du projet peut supprimer un contributeur.")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsCommentAuthor]


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)  # Limite à l'utilisateur connecté

    def perform_destroy(self, instance):
        instance.delete()  # Supprime l'utilisateur et ses données
