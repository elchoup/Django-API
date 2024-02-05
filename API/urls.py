"""
URL configuration for API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers
from user.views import CreateUserView

from project import views
from user.views import UserView

router = routers.DefaultRouter()
router.register(r"users", UserView)
router.register(r"projects", views.ProjectViewSet)
router.register(r"issues", views.IssueViewset)
router.register(r"comments", views.CommentViewset)
router.register(r"contributors", views.ContributorViewset)
project_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
project_router.register(r"issues", views.IssueViewset)
issue_router = routers.NestedDefaultRouter(project_router, r"issues", lookup="issue")
issue_router.register(r"comments", views.CommentViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(issue_router.urls)),
    path(
        "create_user/", CreateUserView.as_view({"post": "create"}), name="create-user"
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
]
