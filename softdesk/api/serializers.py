from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from django.contrib.auth import get_user_model


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']


class IssueSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    contributors = UserSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = '__all__'

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())  # Link to a specific issue
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Auto-assign current user as author
    project = serializers.SerializerMethodField()  # Project information based on the issue

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'issue', 'author', 'project']

    def get_project(self, obj):
        return ProjectSerializer(obj.issue.project).data  # Get project info from the related issue




