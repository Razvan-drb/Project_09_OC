from django.contrib.auth import get_user_model
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

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]


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
