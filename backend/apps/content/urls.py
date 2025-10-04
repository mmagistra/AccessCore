from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'reports', views.ReportViewSet, basename='report')

app_name = 'content'

urlpatterns = [
    path('', include(router.urls)),
]

