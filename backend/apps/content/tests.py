from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.custom_auth.models import CustomUser, Role, BusinessElement, AccessRule
from apps.content.models import Project, Task, Report


class BusinessEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.setup_roles_and_permissions()
        self.setup_users()
        self.setup_business_data()

    def setup_roles_and_permissions(self):
        self.admin_role = Role.objects.create(name='admin@test.com')
        self.manager_role = Role.objects.create(name='manager@test.com')
        self.user_role = Role.objects.create(name='user@test.com')

        self.projects_element = BusinessElement.objects.create(name='projects')
        self.tasks_element = BusinessElement.objects.create(name='tasks')
        self.reports_element = BusinessElement.objects.create(name='reports')

        for element in [self.projects_element, self.tasks_element, self.reports_element]:
            AccessRule.objects.create(
                role=self.admin_role, element=element,
                read_all_permission=True, create_permission=True,
                update_all_permission=True, delete_all_permission=True
            )

        AccessRule.objects.create(
            role=self.manager_role, element=self.projects_element,
            read_all_permission=True, create_permission=True, update_all_permission=True
        )
        AccessRule.objects.create(
            role=self.manager_role, element=self.tasks_element,
            read_all_permission=True, create_permission=True, update_own_permission=True
        )
        AccessRule.objects.create(
            role=self.manager_role, element=self.reports_element,
            read_all_permission=True, create_permission=True, update_own_permission=True
        )

        AccessRule.objects.create(
            role=self.user_role, element=self.projects_element,
            read_own_permission=True, create_permission=True, update_own_permission=True, delete_own_permission=True
        )
        AccessRule.objects.create(
            role=self.user_role, element=self.tasks_element,
            read_own_permission=True, create_permission=True, update_own_permission=True, delete_own_permission=True
        )
        AccessRule.objects.create(
            role=self.user_role, element=self.reports_element,
            read_own_permission=True
        )

    def setup_users(self):
        self.admin_user = CustomUser.objects.create(email='admin@test.com', first_name='Admin@test.com')
        self.admin_user.set_password('admin123')
        self.admin_user.save()
        self.admin_user.roles.add(self.admin_role)

        self.manager_user = CustomUser.objects.create(email='manager@test.com', first_name='Manager@test.com')
        self.manager_user.set_password('manager123')
        self.manager_user.save()
        self.manager_user.roles.add(self.manager_role)

        self.regular_user = CustomUser.objects.create(email='user@test.com', first_name='User@test.com')
        self.regular_user.set_password('user123')
        self.regular_user.save()
        self.regular_user.roles.add(self.user_role)

    def setup_business_data(self):
        self.admin_project = Project.objects.create(
            title='Admin Project', description='Admin project', owner=self.admin_user
        )
        self.user_project = Project.objects.create(
            title='User Project', description='User project', owner=self.regular_user
        )
        self.admin_task = Task.objects.create(
            title='Admin Task', description='Admin task', assignee=self.admin_user
        )
        self.user_task = Task.objects.create(
            title='User Task', description='User task', assignee=self.regular_user
        )
        self.admin_report = Report.objects.create(
            title='Admin Report', content='Admin report content', author=self.admin_user
        )

    def get_token(self, email, password):
        response = self.client.post('/api/auth/login/', {'email': email, 'password': password})
        return response.data['token'] if response.status_code == 200 else None

    def test_projects_list_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_projects_list_user(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_projects_create_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'New Project', 'description': 'New project description', 'status': 'active'}
        response = self.client.post('/api/v1/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_projects_create_user(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'User New Project', 'description': 'User project', 'status': 'active'}
        response = self.client.post('/api/v1/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_projects_retrieve_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'/api/v1/projects/{self.admin_project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_projects_update_owner(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'Updated Project', 'description': 'Updated description', 'status': 'active'}
        response = self.client.put(f'/api/v1/projects/{self.user_project.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_projects_update_non_owner_forbidden(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'Hacked Project', 'description': 'Hacked', 'status': 'active'}
        response = self.client.put(f'/api/v1/projects/{self.admin_project.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_projects_delete_admin_all(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(f'/api/v1/projects/{self.user_project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tasks_list_manager(self):
        token = self.get_token('manager@test.com', 'manager123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_tasks_create_user(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'New Task', 'description': 'New task', 'completed': False}
        response = self.client.post('/api/v1/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tasks_update_assignee(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'Updated Task', 'description': 'Updated', 'completed': True}
        response = self.client.put(f'/api/v1/tasks/{self.user_task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tasks_update_non_assignee_manager_forbidden(self):
        token = self.get_token('manager@test.com', 'manager123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'Hacked Task', 'completed': True}
        response = self.client.put(f'/api/v1/tasks/{self.user_task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reports_list_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reports_create_user_forbidden(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'User Report', 'content': 'Report content'}
        response = self.client.post('/api/v1/reports/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reports_create_manager(self):
        token = self.get_token('manager@test.com', 'manager123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'Manager Report', 'content': 'Manager report content', 'is_published': True}
        response = self.client.post('/api/v1/reports/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_access_forbidden(self):
        response = self.client.get('/api/v1/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
