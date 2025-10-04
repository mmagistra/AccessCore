from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from .decorators import require_authentication, require_permission
from .models import CustomUser, AccessRule, Role, BusinessElement
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer, RoleSerializer, \
    AccessRuleSerializer, BusinessElementSerializer
from .swagger_schemas import register_schema, login_schema, logout_schema, profile_schema, \
    business_element_create_schema, business_element_list_schema, access_rule_update_schema, access_rule_create_schema, \
    access_rule_list_schema, role_update_schema, role_create_schema, role_list_schema, role_retrieve_schema, \
    access_rule_retrieve_schema, access_rule_destroy_schema, role_destroy_schema, business_element_retrieve_schema, \
    business_element_destroy_schema, business_element_update_schema, delete_account_schema


class RegisterView(APIView):
    @register_schema
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = user.generate_jwt_token()
            return Response({
                'user': UserSerializer(user).data,
                'token': token,
                'message': 'Пользователь успешно зарегистрирован'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @login_schema
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(email=email, is_active=True)
                if user.check_password(password):
                    token = user.generate_jwt_token()
                    return Response({
                        'user': UserSerializer(user).data,
                        'token': token,
                        'message': 'Успешная авторизация'
                    })
                else:
                    return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    На данном этапе не используется,
    но при желании поменять тип аутентификации на какой-то другой -
    в таком случае эндпоинт может стать обязательным.
    Поэтому оставлю его здесь
    """
    @logout_schema
    def post(self, request):
        return Response({'message': 'Успешный выход из системы'})


class ProfileView(APIView):
    @profile_schema
    def get(self, request):
        if not hasattr(request, 'email') or  request.email is None:
            return Response({'error': 'Требуется авторизация'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = CustomUser.objects.get(email=request.email, is_active=True)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Требуется авторизация'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'user': UserSerializer(user).data
        })


class DeleteAccountView(APIView):
    @delete_account_schema
    def delete(self, request):
        if not hasattr(request, 'email') or not request.email:
            return Response({'error': 'Требуется авторизация'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = CustomUser.objects.get(email=request.email, is_active=True)
            user.is_active = False
            user.save()

            return Response({
                'message': 'Аккаунт успешно деактивирован',
                'deleted_user_email': user.email
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(require_authentication, name='dispatch')
class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer

    def get_queryset(self):
        try:
            user_roles = CustomUser.objects.get(email=self.request.email, is_active=True).roles.all()
        except CustomUser.DoesNotExist:
            return Role.objects.none()

        has_read_all = AccessRule.objects.filter(
            role__in=user_roles,
            element__name='roles',
            read_all_permission=True
        ).exists()

        if has_read_all:
            return Role.objects.all()
        else:
            return Role.objects.none()

    @role_list_schema
    @require_permission('roles', 'read_all_permission')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @role_retrieve_schema
    @require_permission('roles', 'read_all_permission')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @role_create_schema
    @require_permission('roles', 'create_permission')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_update_schema
    @require_permission('roles', 'update_all_permission')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_update_schema
    @require_permission('roles', 'update_all_permission')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @role_destroy_schema
    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Удаление ролей запрещено'}, status=status.HTTP_403_FORBIDDEN)


@method_decorator(require_authentication, name='dispatch')
class AccessRuleViewSet(viewsets.ModelViewSet):
    serializer_class = AccessRuleSerializer

    def get_queryset(self):
        try:
            user_roles = CustomUser.objects.get(email=self.request.email, is_active=True).roles.all()
        except CustomUser.DoesNotExist:
            return AccessRule.objects.none()

        has_read_all = AccessRule.objects.filter(
            role__in=user_roles,
            element__name='access_rules',
            read_all_permission=True
        ).exists()

        if has_read_all:
            return AccessRule.objects.all()
        else:
            return AccessRule.objects.none()

    @access_rule_list_schema
    @require_permission('access_rules', 'read_all_permission')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @access_rule_retrieve_schema
    @require_permission('access_rules', 'read_all_permission')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @access_rule_create_schema
    @require_permission('access_rules', 'create_permission')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @access_rule_update_schema
    @require_permission('access_rules', 'update_all_permission')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @access_rule_update_schema
    @require_permission('access_rules', 'update_all_permission')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @access_rule_destroy_schema
    @require_permission('access_rules', 'delete_all_permission')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@method_decorator(require_authentication, name='dispatch')
class BusinessElementViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessElementSerializer

    def get_queryset(self):
        try:
            user_roles = CustomUser.objects.get(email=self.request.email, is_active=True).roles.all()
        except CustomUser.DoesNotExist:
            return BusinessElement.objects.none()

        has_read_all = AccessRule.objects.filter(
            role__in=user_roles,
            element__name='business_elements',
            read_all_permission=True
        ).exists()

        if has_read_all:
            return BusinessElement.objects.all()
        else:
            return BusinessElement.objects.none()

    @business_element_list_schema
    @require_permission('business_elements', 'read_all_permission')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @business_element_retrieve_schema
    @require_permission('business_elements', 'read_all_permission')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @business_element_create_schema
    @require_permission('business_elements', 'create_permission')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @business_element_update_schema
    @require_permission('business_elements', 'update_all_permission')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @business_element_update_schema
    @require_permission('business_elements', 'update_all_permission')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @business_element_destroy_schema
    @require_permission('business_elements', 'delete_all_permission')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

