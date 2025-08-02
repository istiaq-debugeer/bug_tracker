from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import status

from .models import Project, Bug, Comment
from .serializers import ProjectSerializer, BugSerializer, CommentSerializer, UserRegisterSerializer
from .utils import log_and_notify, notify_project


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class BugViewSet(viewsets.ModelViewSet):

    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["status"]

    def get_queryset(self):
        queryset = Bug.objects.select_related("created_by", "project").all()
        project_name = self.request.query_params.get("project")
        if project_name:
            queryset = queryset.filter(project__name__icontains=project_name)
        return queryset

    def perform_create(self, serializer):
        bug = serializer.save(created_by=self.request.user)
        notify_project(
            projects_id=bug.project.id,
            message_data={
                "event": "bug_created",
                "bug_id": bug.id,
                "title": bug.title,
                "status": bug.status,
            },
        )

        log_and_notify(
            project_id=bug.project.id,
            user=self.request.user,
            event="bug_created",
            bug=bug,
            message=f"Bug created: {bug.title}",
        )

    def perform_update(self, serializer):
        bug = serializer.save()
        notify_project(
            projects_id=bug.project.id,
            message_data={
                "event": "bug_updated",
                "bug_id": bug.id,
                "title": bug.title,
                "status": bug.status,
            },
        )

        log_and_notify(
            project_id=bug.project.id,
            user=self.request.user,
            event="bug_updated",
            bug=bug,
            message=f"Bug updated: {bug.title}",
        )


class ListBugsApiview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        user_id = kwargs.get("user_id")
        query = (
            Bug.objects.filter(assigned_to=user_id)
            .select_related("assigned_to", "project", "created_by")
            .all()
        )
        serializer = BugSerializer(query, many=True)
        return Response(
            {"message": "Create successfully", "data": serializer.data}, status=200
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related(
        "commenter",
        "bug",
        "bug__project",
        "bug__assigned_to",
        "bug__created_by",
    ).all()
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(commenter=self.request.user)
        bug_object = comment.bug
        user_ids = set()
        if bug_object.created_by:
            user_ids.add(bug_object.created_by.id)
        if bug_object.assign_to:
            user_ids.add(bug_object.assign_to.id)
        notify_project(
            user_ids,
            message_data={
                "event": "comment_added",
                "bug_id": comment.bug.id,
                "title": comment.message,
                "status": comment.bug.status,
            },
        )

        log_and_notify(
            project_id=comment.bug.project.id,
            user=self.request.user,
            event="comment_added",
            bug=comment.bug,
            message=f"New comment: {comment.message}",
        )
