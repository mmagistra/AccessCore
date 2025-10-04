from django.core.management.base import BaseCommand
from apps.custom_auth.models import Role, BusinessElement, AccessRule


class Command(BaseCommand):
    help = 'Создание обновленных тестовых ролей и разрешений'

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(name='admin')
        manager_role, _ = Role.objects.get_or_create(name='manager')
        user_role, _ = Role.objects.get_or_create(name='user')

        projects_element, _ = BusinessElement.objects.get_or_create(name='projects')
        tasks_element, _ = BusinessElement.objects.get_or_create(name='tasks')
        reports_element, _ = BusinessElement.objects.get_or_create(name='reports')
        roles_element, _ = BusinessElement.objects.get_or_create(name='roles')
        access_rules_element, _ = BusinessElement.objects.get_or_create(name='access_rules')
        business_elements_element, _ = BusinessElement.objects.get_or_create(name='business_elements')

        # Права администратора (может все)
        for element in [projects_element, tasks_element, reports_element, roles_element, access_rules_element,
                        business_elements_element]:
            AccessRule.objects.get_or_create(
                role=admin_role, element=element,
                defaults={
                    'read_own_permission': True, 'read_all_permission': True,
                    'create_permission': True,
                    'update_own_permission': True, 'update_all_permission': True,
                    'delete_own_permission': True, 'delete_all_permission': True
                }
            )

        # Права менеджера (не может удалять проекты)
        AccessRule.objects.get_or_create(
            role=manager_role, element=projects_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': True,
                'create_permission': True,
                'update_own_permission': True, 'update_all_permission': True,
                'delete_own_permission': False, 'delete_all_permission': False
            }
        )

        # Права менеджера (может добавлять, читать задачи и редактировать/удалять свои)
        AccessRule.objects.get_or_create(
            role=manager_role, element=tasks_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': True,
                'create_permission': True,
                'update_own_permission': True, 'update_all_permission': False,
                'delete_own_permission': True, 'delete_all_permission': False
            }
        )

        # Права менеджера (может добавлять, читать отчеты и редактировать/удалять свои)
        AccessRule.objects.get_or_create(
            role=manager_role, element=reports_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': True,
                'create_permission': True,
                'update_own_permission': True, 'update_all_permission': False,
                'delete_own_permission': True, 'delete_all_permission': False
            }
        )

        # Права менеджера (может читать роли)
        AccessRule.objects.get_or_create(
            role=manager_role, element=roles_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': True,
                'create_permission': False,
                'update_own_permission': False, 'update_all_permission': False,
                'delete_own_permission': False, 'delete_all_permission': False
            }
        )

        # Права менеджера (может читать правила доступа)
        AccessRule.objects.get_or_create(
            role=manager_role, element=access_rules_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': True,
                'create_permission': False,
                'update_own_permission': False, 'update_all_permission': False,
                'delete_own_permission': False, 'delete_all_permission': False
            }
        )

        # Права менеджера (может читать элементы бизнеса)
        AccessRule.objects.get_or_create(
            role=manager_role, element=business_elements_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': True,
                'create_permission': False,
                'update_own_permission': False, 'update_all_permission': False,
                'delete_own_permission': False, 'delete_all_permission': False
            }
        )

        # Права пользователя (CRUD только для своих проектов)
        AccessRule.objects.get_or_create(
            role=user_role, element=projects_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': False,
                'create_permission': True,
                'update_own_permission': True, 'update_all_permission': False,
                'delete_own_permission': True, 'delete_all_permission': False
            }
        )

        # Права пользователя (CRUD только для своих задач)
        AccessRule.objects.get_or_create(
            role=user_role, element=tasks_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': False,
                'create_permission': True,
                'update_own_permission': True, 'update_all_permission': False,
                'delete_own_permission': True, 'delete_all_permission': False
            }
        )

        # Права пользователя (может читать свои отчеты)
        AccessRule.objects.get_or_create(
            role=user_role, element=reports_element,
            defaults={
                'read_own_permission': True, 'read_all_permission': False,
                'create_permission': False,
                'update_own_permission': False, 'update_all_permission': False,
                'delete_own_permission': False, 'delete_all_permission': False
            }
        )

        self.stdout.write(self.style.SUCCESS('Тестовые роли созданы!'))
