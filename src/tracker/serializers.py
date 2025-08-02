from rest_framework import serializers
from .models import Project, Bug, Comment
from django.contrib.auth.models import User


from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Use email as username
        user = User.objects.create_user(
            username=validated_data['email'],  # username is required, use email as username
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "created_at", "updated_at"]


class GetBugSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    priority = serializers.CharField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BugSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), write_only=True, source="project"
    )
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Bug
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "project",
            "project_id",
            "created_by",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserSerializer(read_only=True)
    bug = GetBugSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "bug", "commenter", "message", "created_at", "updated_at"]
