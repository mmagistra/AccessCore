from django.core.management.base import BaseCommand
from apps.custom_auth.models import CustomUser, Role


class Command(BaseCommand):
    help = 'Создание тестовых данных для демонстрации прав доступа'

    def handle(self, *args, **options):
        # Получаем роли
        try:
            admin_role = Role.objects.get(name='admin')
            manager_role = Role.objects.get(name='manager')
            user_role = Role.objects.get(name='user')
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR('Роли не созданы'))
            return

        # Создаем тестовых пользователей
        admin_user, created = CustomUser.objects.get_or_create(
            email='admin@test.com',
            defaults={'first_name': 'Админ', 'last_name': 'Админов'}
        )
        if created:
            admin_user.roles.add(admin_role)
        admin_user.set_password('admin123')
        admin_user.save()

        manager_user, created = CustomUser.objects.get_or_create(
            email='manager@test.com',
            defaults={'first_name': 'Менеджер', 'last_name': 'Менеджеров'}
        )
        if created:
            manager_user.roles.add(manager_role)
        manager_user.set_password('manager123')
        manager_user.save()

        user_user, created = CustomUser.objects.get_or_create(
            email='user@test.com',
            defaults={'first_name': 'Пользователь', 'last_name': 'Пользователев'}
        )
        if created:
            user_user.roles.add(user_role)
        user_user.set_password('user123')
        user_user.save()

        self.stdout.write(self.style.SUCCESS('Созданы 3 пользователя:'))
        self.stdout.write(self.style.SUCCESS('Admin: admin@test.com / admin123'))
        self.stdout.write(self.style.SUCCESS('Manager: manager@test.com / manager123'))
        self.stdout.write(self.style.SUCCESS('User: user@test.com / user123'))
