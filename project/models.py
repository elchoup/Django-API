from django.db import models
from django.conf import settings
import uuid


# Create your models here.
class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributor",
    )


class Project(models.Model):
    class Type(models.TextChoices):
        BACKEND = "backend"
        FRONTEND = "frontend"
        IOS = "ios"
        ANDROID = "android"

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_project",
    )
    contributors = models.ManyToManyField(
        Contributor, related_name="contributor_project", blank=True
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.BACKEND)


class Issue(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW"
        MEDIUM = "MED"
        HIGH = "HIG"

    class Tag(models.TextChoices):
        BUG = "BUG"
        FEATURE = "FEA", "Feature"
        TASK = "TAS", "Task"

    class Status(models.TextChoices):
        TODO = "TDO", "To do"
        INPROGRESS = "INP", "In progress"
        FINISHED = "FIN", "FInished"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    priority = models.CharField(
        max_length=3, choices=Priority.choices, default=Priority.LOW
    )
    tag = models.CharField(max_length=3, choices=Tag.choices, default=Tag.BUG)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.TODO)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    link = models.URLField()
    unique_identifier = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
