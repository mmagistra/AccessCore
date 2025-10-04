from django.db import models

from django.db import models
from apps.custom_auth.models import CustomUser


class Project(models.Model):
    """
    Модель проектов - полная демонстрация RBAC

    Права доступа:
    - Admin: полный доступ ко всем проектам
    - Manager: чтение всех + редактирование всех
    - User: только свои проекты (CRUD)
    """
    title = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=20, default='active', verbose_name='Статус')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.owner.email})"


class Task(models.Model):
    """
    Модель задач - смешанные права доступа

    Права доступа:
    - Admin: полный доступ ко всем задачам
    - Manager: чтение всех + редактирование только своих
    - User: только свои задачи (CRUD)
    """
    title = models.CharField(max_length=200, verbose_name='Название задачи')
    description = models.TextField(blank=True, verbose_name='Описание')
    completed = models.BooleanField(default=False, verbose_name='Выполнено')
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.assignee.first_name}"


class Report(models.Model):
    """
    Модель отчетов - ограниченные права для пользователей

    Права доступа:
    - Admin: полный доступ ко всем отчетам
    - Manager: чтение всех + создание/редактирование своих
    - User: только чтение своих отчетов
    """
    title = models.CharField(max_length=200, verbose_name='Название отчета')
    content = models.TextField(verbose_name='Содержание отчета')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.first_name}"

