from functools import wraps
from django.http import JsonResponse
from .models import AccessRule, CustomUser


def require_authentication(view_func):
    """Декоратор для проверки аутентификации"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'email') or not request.email:
            return JsonResponse({
                'error': 'Требуется авторизация',
                'message': 'Для доступа к этому ресурсу необходимо предоставить действительный JWT токен',
                'code': 'AUTHENTICATION_REQUIRED'
            }, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


def require_permission(element_name, permission_type):
    """Декоратор для проверки прав доступа к ресурсу"""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.request, 'email') or not request.request.email:
                return JsonResponse({'error': 'Требуется авторизация'}, status=401)
            try:
                user = CustomUser.objects.get(email=request.request.email, is_active=True)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Пользователь не найден'}, status=401)

            # Получаем роли пользователя через ManyToMany
            user_roles = user.roles.all()

            if not user_roles.exists():
                return JsonResponse({
                    'error': 'У пользователя нет назначенных ролей'
                }, status=403)

            has_permission = AccessRule.objects.filter(
                role__in=user_roles,
                element__name=element_name,
                **{permission_type: True}
            ).exists()

            if not has_permission:
                return JsonResponse({
                    'error': 'Доступ запрещен',
                    'message': f'У вас не достаточно для доступа к ресурсу',
                    'required_permission': permission_type,
                    'resource': element_name
                }, status=403)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_ownership_or_permission(element_name, permission_type, ownership_field):
    """
    Декоратор для проверки владения объектом ИЛИ специального разрешения

    Args:
        element_name: Название бизнес-элемента
        permission_type: Тип разрешения (например, update_all_permission)
        ownership_field: Поле для проверки владения (например, 'owner', 'assignee', 'author')
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not hasattr(request, 'email') or not request.email:
                return JsonResponse({'error': 'Требуется авторизация'}, status=401)

            try:
                user = CustomUser.objects.get(email=request.email, is_active=True)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Пользователь не найден'}, status=401)

            obj = self.get_object()
            user_roles = user.roles.all()

            has_all_permission = AccessRule.objects.filter(
                role__in=user_roles,
                element__name=element_name,
                **{permission_type: True}
            ).exists()

            if has_all_permission:
                return view_func(self, request, *args, **kwargs)

            # Проверяем права на свои объекты + владение
            own_permission_type = permission_type.replace('_all_', '_own_')
            has_own_permission = AccessRule.objects.filter(
                role__in=user_roles,
                element__name=element_name,
                **{own_permission_type: True}
            ).exists()

            if has_own_permission and getattr(obj, ownership_field) == user:
                return view_func(self, request, *args, **kwargs)

            return JsonResponse({
                'error': 'Доступ запрещен',
                'message': f'У вас не достаточно для доступа к ресурсу',
            }, status=403)

        return wrapper

    return decorator
