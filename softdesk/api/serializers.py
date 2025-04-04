from datetime import date

from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'email', 'can_be_contacted', 'can_data_be_shared']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Ensure password is writable but not returned
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label="Confirm Password")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'birth_date', 'can_be_contacted', 'can_data_be_shared']

    def validate(self, data):
        """ Ensure the two passwords match """
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Les mots de passe ne correspondent pas."})
        return data

    def validate_birth_date(self, value):
        """ Vérifie si l'utilisateur a au moins 18 ans """
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        if age < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour créer un compte.")
        return value

    def create(self, validated_data):
        """ Crée un utilisateur avec un mot de passe correctement haché """
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # Hash password
        user.save()
        return user

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




