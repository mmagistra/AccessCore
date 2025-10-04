from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.custom_auth.models import CustomUser, Role, BusinessElement, AccessRule


class AuthEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.setup_roles_and_permissions()
        self.setup_users()

    def setup_roles_and_permissions(self):
        self.admin_role = Role.objects.create(name='admin@test.com', description='Administrator')
        self.manager_role = Role.objects.create(name='manager@test.com', description='Manager@test.com')
        self.user_role = Role.objects.create(name='user@test.com', description='Regular user')

        self.roles_element = BusinessElement.objects.create(name='roles')
        self.access_rules_element = BusinessElement.objects.create(name='access_rules')
        self.business_elements_element = BusinessElement.objects.create(name='business_elements')

        AccessRule.objects.create(
            role=self.admin_role, element=self.roles_element,
            read_all_permission=True, create_permission=True, update_all_permission=True
        )
        AccessRule.objects.create(
            role=self.admin_role, element=self.access_rules_element,
            read_all_permission=True, create_permission=True, update_all_permission=True, delete_all_permission=True
        )
        AccessRule.objects.create(
            role=self.admin_role, element=self.business_elements_element,
            read_all_permission=True, create_permission=True, update_all_permission=True, delete_all_permission=True
        )
        AccessRule.objects.create(
            role=self.manager_role, element=self.roles_element,
            read_all_permission=True
        )
        AccessRule.objects.create(
            role=self.manager_role, element=self.access_rules_element,
            read_all_permission=True
        )

    def setup_users(self):
        self.admin_user = CustomUser.objects.create(email='admin@test.com', first_name='Admin')
        self.admin_user.set_password('admin123')
        self.admin_user.save()
        self.admin_user.roles.add(self.admin_role)

        self.manager_user = CustomUser.objects.create(email='manager@test.com', first_name='Manager')
        self.manager_user.set_password('manager123')
        self.manager_user.save()
        self.manager_user.roles.add(self.manager_role)

        self.regular_user = CustomUser.objects.create(email='user@test.com', first_name='User')
        self.regular_user.set_password('user123')
        self.regular_user.save()
        self.regular_user.roles.add(self.user_role)

    def get_token(self, email, password):
        response = self.client.post('/api/auth/login/', {'email': email, 'password': password})
        return response.data['token'] if response.status_code == 200 else None

    def test_register_success(self):
        data = {
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User@test.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_register_password_mismatch(self):
        data = {
            'email': 'newuser@test.com',
            'first_name': 'New',
            'password': 'newpass123',
            'password_confirm': 'differentpass'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        response = self.client.post('/api/auth/login/', {'email': 'admin@test.com', 'password': 'admin123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/auth/login/', {'email': 'admin@test.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_authenticated(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_profile_unauthenticated(self):
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_roles_list_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roles_list_manager(self):
        token = self.get_token('manager@test.com', 'manager123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roles_list_user_forbidden(self):
        token = self.get_token('user@test.com', 'user123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/roles/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_roles_create_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'newrole', 'description': 'New Role'}
        response = self.client.post('/api/auth/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_roles_create_manager_forbidden(self):
        token = self.get_token('manager@test.com', 'manager123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'newrole', 'description': 'New Role'}
        response = self.client.post('/api/auth/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_roles_update_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'updated_admin', 'description': 'Updated Admin'}
        response = self.client.put(f'/api/auth/roles/{self.admin_role.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_roles_delete_forbidden(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(f'/api/auth/roles/{self.admin_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_rules_list_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/access-rules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_rules_create_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {
            'role_id': self.user_role.id,
            'element_id': self.roles_element.id,
            'read_own_permission': True
        }
        response = self.client.post('/api/auth/access-rules/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_access_rules_update_admin(self):
        rule = AccessRule.objects.first()
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'create_permission': False}
        response = self.client.patch(f'/api/auth/access-rules/{rule.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_elements_list_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/business-elements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_elements_create_admin(self):
        token = self.get_token('admin@test.com', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'newelement', 'description': 'New Element'}
        response = self.client.post('/api/auth/business-elements/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
