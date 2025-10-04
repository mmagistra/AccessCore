from django.core.management.base import BaseCommand
from apps.content.models import Project, Task, Report
from apps.custom_auth.models import CustomUser


class Command(BaseCommand):
    help = 'Создание тестовых данных для демонстрации прав доступа'

    def handle(self, *args, **options):
        try:
            admin_user = CustomUser.objects.get(email='admin@test.com')
            manager_user = CustomUser.objects.get(email='manager@test.com')
            user_user = CustomUser.objects.get(email='user@test.com')
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователи не созданы'))
            return

        # Создаем тестовые проекты
        Project.objects.get_or_create(
            title='Проект Админа',
            defaults={
                'description': 'Проект созданный администратором',
                'owner': admin_user
            }
        )

        Project.objects.get_or_create(
            title='Проект Менеджера',
            defaults={
                'description': 'Проект созданный менеджером',
                'owner': manager_user
            }
        )

        Project.objects.get_or_create(
            title='Проект Пользователя',
            defaults={
                'description': 'Проект созданный обычным пользователем',
                'owner': user_user
            }
        )

        # Создаем тестовые задачи
        Task.objects.get_or_create(
            title='Задача для Админа',
            defaults={
                'description': 'Задача назначенная администратору',
                'assignee': admin_user
            }
        )

        Task.objects.get_or_create(
            title='Задача для Менеджера',
            defaults={
                'description': 'Задача назначенная менеджеру',
                'assignee': manager_user
            }
        )

        Task.objects.get_or_create(
            title='Задача для Пользователя',
            defaults={
                'description': 'Задача назначенная обычному пользователю',
                'assignee': user_user
            }
        )

        # Создаем тестовые отчеты
        Report.objects.get_or_create(
            title='Отчет от Админа',
            defaults={
                'content': 'Отчет созданный администратором системы',
                'author': admin_user
            }
        )

        Report.objects.get_or_create(
            title='Отчет от Менеджера',
            defaults={
                'content': 'Отчет созданный менеджером',
                'author': manager_user
            }
        )

        Report.objects.get_or_create(
            title='Отчет от Пользователя',
            defaults={
                'content': 'Отчет созданный обычным пользователем',
                'author': user_user
            }
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные созданы!'))
