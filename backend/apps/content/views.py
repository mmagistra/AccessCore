from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Project, Task, Report
from .serializers import ProjectSerializer, TaskSerializer, ReportSerializer
from apps.custom_auth.decorators import require_authentication, require_permission, require_ownership_or_permission
from apps.custom_auth.models import AccessRule, CustomUser
from django.utils.decorators import method_decorator
from .swagger_schemas import *


@method_decorator(require_authentication, name='dispatch')
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        try:
            self.email = self.request.email
        except AttributeError:
            self.email = None
        try:
            user = CustomUser.objects.get(email=self.request.email, is_active=True)
        except CustomUser.DoesNotExist:
            return Project.objects.none()

        user_roles = user.roles.all()

        has_read_all = AccessRule.objects.filter(
            role__in=user_roles,
            element__name='projects',
            read_all_permission=True
        ).exists()

        if has_read_all:
            return Project.objects.all()
        else:
            return Project.objects.filter(owner=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self.request, 'email') and self.request.email:
            try:
                context['user'] = CustomUser.objects.get(email=self.request.email)
            except CustomUser.DoesNotExist:
                pass
        return context

    @project_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @project_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @project_create_schema
    @require_permission('projects', 'create_permission')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @project_update_schema
    @require_ownership_or_permission('projects', 'update_all_permission', 'owner')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @project_update_schema
    @require_ownership_or_permission('projects', 'update_all_permission', 'owner')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @project_destroy_schema
    @require_ownership_or_permission('projects', 'delete_all_permission', 'owner')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@method_decorator(require_authentication, name='dispatch')
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        try:
            user = CustomUser.objects.get(email=self.request.email, is_active=True)
        except CustomUser.DoesNotExist:
            return Task.objects.none()

        user_roles = user.roles.all()

        has_read_all = AccessRule.objects.filter(
            role__in=user_roles,
            element__name='tasks',
            read_all_permission=True
        ).exists()

        if has_read_all:
            return Task.objects.all()
        else:
            return Task.objects.filter(assignee=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self.request, 'email') and self.request.email:
            try:
                context['user'] = CustomUser.objects.get(email=self.request.email)
            except CustomUser.DoesNotExist:
                pass
        return context

    @task_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @task_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @task_create_schema
    @require_permission('tasks', 'create_permission')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @task_update_schema
    @require_ownership_or_permission('tasks', 'update_all_permission', 'assignee')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @task_update_schema
    @require_ownership_or_permission('tasks', 'update_all_permission', 'assignee')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @task_destroy_schema
    @require_ownership_or_permission('tasks', 'delete_all_permission', 'assignee')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@method_decorator(require_authentication, name='dispatch')
class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        try:
            user = CustomUser.objects.get(email=self.request.email, is_active=True)
        except CustomUser.DoesNotExist:
            return Report.objects.none()

        user_roles = user.roles.all()

        has_read_all = AccessRule.objects.filter(
            role__in=user_roles,
            element__name='reports',
            read_all_permission=True
        ).exists()

        if has_read_all:
            return Report.objects.all()
        else:
            return Report.objects.filter(author=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self.request, 'email') and self.request.email:
            try:
                context['user'] = CustomUser.objects.get(email=self.request.email)
            except CustomUser.DoesNotExist:
                pass
        return context

    @report_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @report_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @report_create_schema
    @require_permission('reports', 'create_permission')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @report_update_schema
    @require_ownership_or_permission('reports', 'update_all_permission', 'author')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @report_update_schema
    @require_ownership_or_permission('reports', 'update_all_permission', 'author')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @report_destroy_schema
    @require_ownership_or_permission('reports', 'delete_all_permission', 'author')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
