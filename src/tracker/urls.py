from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, BugViewSet, CommentViewSet, ListBugsApiview
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"bugs", BugViewSet, basename="bugs")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
    path("my-bugs/<int:user_id>/", ListBugsApiview.as_view(), name="my-bugs"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
