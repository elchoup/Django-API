from rest_framework import serializers

from . import models
from user.serializers import UserSerializer


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Contributor
        fields = ["user"]


class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=models.Project.Type.choices, default=models.Project.Type.BACKEND
    )

    class Meta:
        model = models.Project
        fields = [
            "id",
            "title",
            "description",
            "type",
        ]


class IssueSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    author = UserSerializer()

    priority = serializers.ChoiceField(
        choices=models.Issue.Priority.choices, default=models.Issue.Priority.LOW
    )
    tag = serializers.ChoiceField(
        choices=models.Issue.Tag.choices, default=models.Issue.Tag.BUG
    )
    status = serializers.ChoiceField(
        choices=models.Issue.Status.choices, default=models.Issue.Status.TODO
    )

    class Meta:
        model = models.Issue
        fields = [
            "id",
            "project",
            "author",
            "name",
            "description",
            "priority",
            "tag",
            "status",
        ]


class CommentSerializer(serializers.ModelSerializer):
    issue = IssueSerializer()
    author = UserSerializer()

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "issue",
            "author",
            "description",
            "link",
            "unique_identifier",
        ]
