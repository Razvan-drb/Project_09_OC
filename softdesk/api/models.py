from datetime import date

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings



class Project(models.Model):
    BACKEND = 'back-end'
    FRONTEND = 'front-end'
    IOS = 'iOS'
    ANDROID = 'android'

    PROJECT_TYPES = [
        (BACKEND, 'Back-End'),
        (FRONTEND, 'Front-End'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="contributors")

    def __str__(self):
        return f"{self.user.username} -> {self.project.name}"

class Issue(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'

    TAG_CHOICES = [
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
        (TASK, 'Task'),
    ]

    TODO = 'To Do'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'

    STATUS_CHOICES = [
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=MEDIUM)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default=TASK)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=TODO)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="issues")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="assigned_issues")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_issues")
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="contributed_issues", blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    issue = models.ForeignKey("Issue", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"


#
# class CustomUser(AbstractUser):
#     can_be_contacted = models.BooleanField(default=False)
#     can_data_be_shared = models.BooleanField(default=False)
#
#     # Correction pour éviter les conflits
#     groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=False)  # Champ obligatoire
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    # Correction pour éviter les conflits
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def age(self):
        """Retourne l'âge de l'utilisateur."""
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
