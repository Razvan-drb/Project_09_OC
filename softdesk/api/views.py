from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, CommentSerializer, ContributorSerializer, UserSerializer, \
    IssueWriteSerializer, IssueReadSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsAuthorOrReadOnly, IsProjectContributor, IsCommentAuthor
from rest_framework.decorators import action
from rest_framework.response import Response


User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

# class IssueViewSet(viewsets.ModelViewSet):
#     queryset = Issue.objects.all()
#     permission_classes = [IsAuthenticated, IsProjectContributor]
#
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return IssueWriteSerializer
#         return IssueReadSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return IssueReadSerializer
        return IssueWriteSerializer

    permission_classes = [IsAuthenticated, IsProjectContributor]

    @action(detail=True, methods=['post'], url_path='add_contributor')
    def add_contributor(self, request, pk=None):
        issue = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"detail": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        issue.contributors.add(user)
        issue.save()

        # Return updated issue data with contributors
        serializer = IssueReadSerializer(issue, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthenticated]#[AllowAny]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)  # Limite à l'utilisateur connecté

    def perform_destroy(self, instance):
        instance.delete()  # Supprime l'utilisateur et ses données

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("Vous ne pouvez accéder ou modifier que votre propre compte.")
        return obj
