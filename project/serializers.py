from rest_framework import serializers

from . import models
from user.serializers import UserSerializer


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
            "author",
            "contributors",
            "created_time",
        ]
        read_only_fields = ["author", "contributors", "created_time"]


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = models.Contributor
        fields = ["id", "user", "project"]


class IssueSerializer(serializers.ModelSerializer):
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
            "name",
            "description",
            "priority",
            "tag",
            "status",
            "author",
            "project",
            "created_time",
        ]
        read_only_fields = [
            "author",
            "project",
            "created_time",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "description",
            "author",
            "issue",
            "link",
            "created_time",
        ]
        read_only_fields = [
            "author",
            "issue",
            "unique_identifier",
            "created_time",
        ]
