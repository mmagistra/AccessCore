from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    UserSerializer,
    RoleSerializer,
    AccessRuleSerializer,
    BusinessElementSerializer
)

user_response_example = {
    "application/json": {
        "user": {
            "id": 1,
            "email": "user@example.com",
            "first_name": "Иван",
            "last_name": "Петров"
        },
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "message": "Пользователь успешно зарегистрирован"
    }
}

profile_response_example = {
    "application/json": {
        "user": {
            "id": 1,
            "email": "user@example.com",
            "first_name": "Иван",
            "last_name": "Петров",
            "created_at": "2025-01-01T12:00:00Z"
        }
    }
}

# Декораторы для аутентификации
register_schema = swagger_auto_schema(
    operation_id='auth_register',
    operation_summary='Регистрация пользователя',
    operation_description='''
    Регистрирует нового пользователя в системе.

    **Требования:**
    - Email должен быть уникальным
    - Пароль минимум 6 символов
    - Пароли должны совпадать

    **Возвращает:**
    - Информацию о пользователе
    - JWT токен для аутентификации
    ''',
    request_body=UserRegistrationSerializer,
    responses={
        201: openapi.Response(
            description="Пользователь успешно зарегистрирован",
            examples=user_response_example
        ),
        400: "Ошибки валидации"
    },
    tags=['Аутентификация']
)

login_schema = swagger_auto_schema(
    operation_id='auth_login',
    operation_summary='Вход в систему',
    operation_description='''
    Аутентификация пользователя по email и паролю.

    **Возвращает JWT токен** для дальнейшего использования в заголовке Authorization.

    Пример использования токена:
    ```
    Authorization: Bearer <полученный_токен>
    ```
    ''',
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Успешная аутентификация",
            examples=user_response_example
        ),
        401: "Неверные учетные данные"
    },
    tags=['Аутентификация']
)

logout_schema = swagger_auto_schema(
    operation_id='auth_logout',
    operation_summary='Выход из системы',
    operation_description='''
    Выход пользователя из системы.

    **Примечание:** При JWT аутентификации клиент должен самостоятельно 
    удалить токен из локального хранилища.
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={}
    ),
    responses={
        200: openapi.Response(
            description="Успешный выход",
            examples={
                "application/json": {
                    "message": "Успешный выход из системы"
                }
            }
        )
    },
    tags=['Аутентификация']
)

profile_schema = swagger_auto_schema(
    operation_id='auth_profile',
    operation_summary='Профиль пользователя',
    operation_description='''
    Получение информации о текущем аутентифицированном пользователе.

    **Требует авторизации:** JWT токен в заголовке Authorization.
    ''',
    responses={
        200: openapi.Response(
            description="Информация о пользователе",
            examples=profile_response_example
        ),
        401: "Требуется авторизация"
    },
    tags=['Пользователь']
)

delete_account_schema = swagger_auto_schema(
    operation_id='auth_delete_account',
    operation_summary='Удаление собственного аккаунта',
    operation_description='''
    Мягкое удаление аккаунта текущего пользователя.

    Аккаунт деактивируется (is_active = False), но данные остаются в базе данных.
    После удаления пользователь не сможет войти в систему.
    ''',
    responses={
        200: openapi.Response(
            description="Аккаунт успешно деактивирован",
            examples={
                "application/json": {
                    "message": "Аккаунт успешно деактивирован",
                    "deleted_user_email": "user@example.com"
                }
            }
        ),
        401: openapi.Response(
            description="Требуется авторизация",
            examples={
                "application/json": {
                    "error": "Требуется авторизация"
                }
            }
        ),
        404: openapi.Response(
            description="Пользователь не найден",
            examples={
                "application/json": {
                    "error": "Пользователь не найден"
                }
            }
        )
    },
    tags=['Пользователь']
)

# Параметры для списка пользователей
users_list_parameters = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="JWT токен в формате: Bearer <token>",
        type=openapi.TYPE_STRING,
        required=True
    ),
    openapi.Parameter(
        'email',
        openapi.IN_QUERY,
        description="Фильтр по email (частичное совпадение)",
        type=openapi.TYPE_STRING,
        required=False
    ),
    openapi.Parameter(
        'first_name',
        openapi.IN_QUERY,
        description="Фильтр по имени пользователя",
        type=openapi.TYPE_STRING,
        required=False
    ),
    openapi.Parameter(
        'is_active',
        openapi.IN_QUERY,
        description="Фильтр по активности пользователя",
        type=openapi.TYPE_BOOLEAN,
        required=False,
        default=True
    ),
    openapi.Parameter(
        'limit',
        openapi.IN_QUERY,
        description="Количество записей на страницу (по умолчанию 20)",
        type=openapi.TYPE_INTEGER,
        required=False,
        default=20,
        minimum=1,
        maximum=100
    ),
    openapi.Parameter(
        'offset',
        openapi.IN_QUERY,
        description="Смещение для пагинации (по умолчанию 0)",
        type=openapi.TYPE_INTEGER,
        required=False,
        default=0,
        minimum=0
    ),
]

users_list_schema = swagger_auto_schema(
    operation_id='users_list',
    operation_summary='Список пользователей',
    operation_description='Получение списка пользователей с возможностью фильтрации и пагинации',
    manual_parameters=users_list_parameters,
    responses={
        200: openapi.Response(
            description="Список пользователей",
            examples={
                "application/json": {
                    "users": [
                        {
                            "id": 1,
                            "email": "user1@example.com",
                            "first_name": "Иван",
                            "last_name": "Петров",
                            "is_active": True,
                            "created_at": "2025-01-01T12:00:00Z"
                        }
                    ],
                    "count": 1,
                    "total": 15
                }
            }
        ),
        401: "Требуется авторизация"
    },
    tags=['Администрирование']
)

unauthorized_response = openapi.Response(
    description="Требуется авторизация",
    examples={
        "application/json": {
            "error": "Требуется авторизация"
        }
    }
)

forbidden_response = openapi.Response(
    description="Недостаточно прав доступа",
    examples={
        "application/json": {
            "error": "Доступ запрещен"
        }
    }
)

role_list_schema = swagger_auto_schema(
    operation_id='roles_list',
    operation_summary='Список ролей',
    operation_description='Получение списка всех ролей в системе (только для Admin и Manager)',
    responses={
        200: openapi.Response(
            description="Список ролей",
            schema=RoleSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "admin",
                        "description": "Администратор системы",
                        "created_at": "2025-10-04T20:00:00Z"
                    }
                ]
            }
        ),
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

role_create_schema = swagger_auto_schema(
    operation_id='roles_create',
    operation_summary='Создание роли',
    operation_description='Создание новой роли (только для Admin)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, max_length=50, example='moderator'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, example='Модератор контента')
        },
        required=['name']
    ),
    responses={
        201: openapi.Response(description="Роль создана", schema=RoleSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

role_retrieve_schema = swagger_auto_schema(
    operation_id='roles_retrieve',
    operation_summary='Получение роли по ID',
    operation_description='Получение информации о конкретной роли',
    responses={
        200: openapi.Response(description="Данные роли", schema=RoleSerializer),
        404: "Роль не найдена",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

role_update_schema = swagger_auto_schema(
    operation_id='roles_update',
    operation_summary='Обновление роли',
    operation_description='Обновление существующей роли (только для Admin)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, max_length=50),
            'description': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['name']
    ),
    responses={
        200: openapi.Response(description="Роль обновлена", schema=RoleSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Роль не найдена"
    },
    tags=['Администрирование']
)

access_rule_list_schema = swagger_auto_schema(
    operation_id='access_rules_list',
    operation_summary='Список правил доступа',
    operation_description='Получение списка всех правил доступа (только для Admin и Manager)',
    responses={
        200: openapi.Response(
            description="Список правил доступа",
            schema=AccessRuleSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "role": {
                            "id": 1,
                            "name": "admin",
                            "description": "Администратор системы"
                        },
                        "element": {
                            "id": 1,
                            "name": "projects",
                            "description": "Проекты"
                        },
                        "create_permission": True,
                        "read_own_permission": True,
                        "read_all_permission": True,
                        "update_own_permission": True,
                        "update_all_permission": True,
                        "delete_permission": True,
                        "delete_all_permission": True,
                        "created_at": "2025-10-04T20:00:00Z"
                    }
                ]
            }
        ),
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

access_rule_create_schema = swagger_auto_schema(
    operation_id='access_rules_create',
    operation_summary='Создание правила доступа',
    operation_description='Создание нового правила доступа (только для Admin)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'role_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            'element_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            'create_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'read_own_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'read_all_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'update_own_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'update_all_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'delete_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'delete_all_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False)
        },
        required=['role_id', 'element_id']
    ),
    responses={
        201: openapi.Response(description="Правило доступа создано", schema=AccessRuleSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

access_rule_update_schema = swagger_auto_schema(
    operation_id='access_rules_update',
    operation_summary='Обновление правила доступа',
    operation_description='Обновление существующего правила доступа (только для Admin)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'create_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'read_own_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'read_all_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'update_own_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'update_all_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'delete_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'delete_all_permission': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        }
    ),
    responses={
        200: openapi.Response(description="Правило доступа обновлено", schema=AccessRuleSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Правило доступа не найдено"
    },
    tags=['Администрирование']
)

business_element_list_schema = swagger_auto_schema(
    operation_id='business_elements_list',
    operation_summary='Список бизнес-элементов',
    operation_description='Получение списка всех бизнес-элементов (только для Admin и Manager)',
    responses={
        200: openapi.Response(description="Список бизнес-элементов", schema=BusinessElementSerializer(many=True)),
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

business_element_create_schema = swagger_auto_schema(
    operation_id='business_elements_create',
    operation_summary='Создание бизнес-элемента',
    operation_description='Создание нового бизнес-элемента (только для Admin)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, max_length=100, example='comments'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, example='Управление комментариями')
        },
        required=['name']
    ),
    responses={
        201: openapi.Response(description="Бизнес-элемент создан", schema=BusinessElementSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

role_destroy_schema = swagger_auto_schema(
    operation_id='roles_destroy',
    operation_summary='Удаление роли',
    operation_description='Удаление роли запрещено в системе для обеспечения целостности данных',
    responses={
        403: openapi.Response(
            description="Удаление ролей запрещено",
            examples={
                "application/json": {
                    "error": "Удаление ролей запрещено"
                }
            }
        ),
        401: unauthorized_response,
        404: "Роль не найдена"
    },
    tags=['Администрирование']
)

access_rule_retrieve_schema = swagger_auto_schema(
    operation_id='access_rules_retrieve',
    operation_summary='Получение правила доступа по ID',
    operation_description='Получение информации о конкретном правиле доступа',
    responses={
        200: openapi.Response(
            description="Данные правила доступа",
            schema=AccessRuleSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "role": {
                        "id": 1,
                        "name": "admin",
                        "description": "Администратор системы",
                        "created_at": "2025-10-04T20:00:00Z"
                    },
                    "element": {
                        "id": 1,
                        "name": "projects",
                        "description": "Проекты",
                        "created_at": "2025-10-04T20:00:00Z"
                    },
                    "create_permission": True,
                    "read_own_permission": True,
                    "read_all_permission": True,
                    "update_own_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                    "created_at": "2025-10-04T20:00:00Z"
                }
            }
        ),
        404: "Правило доступа не найдено",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

access_rule_destroy_schema = swagger_auto_schema(
    operation_id='access_rules_destroy',
    operation_summary='Удаление правила доступа',
    operation_description='Удаление существующего правила доступа (только для Admin)',
    responses={
        204: "Правило доступа удалено",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Правило доступа не найдено"
    },
    tags=['Администрирование']
)

business_element_retrieve_schema = swagger_auto_schema(
    operation_id='business_elements_retrieve',
    operation_summary='Получение бизнес-элемента по ID',
    operation_description='Получение информации о конкретном бизнес-элементе',
    responses={
        200: openapi.Response(
            description="Данные бизнес-элемента",
            schema=BusinessElementSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "name": "projects",
                    "description": "Управление проектами",
                    "created_at": "2025-10-04T20:00:00Z"
                }
            }
        ),
        404: "Бизнес-элемент не найден",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Администрирование']
)

business_element_update_schema = swagger_auto_schema(
    operation_id='business_elements_update',
    operation_summary='Обновление бизнес-элемента',
    operation_description='Обновление существующего бизнес-элемента (только для Admin)',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                max_length=100,
                example='projects_updated'
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                example='Обновленное управление проектами'
            )
        },
        required=['name']
    ),
    responses={
        200: openapi.Response(
            description="Бизнес-элемент обновлен",
            schema=BusinessElementSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "name": "projects_updated",
                    "description": "Обновленное управление проектами",
                    "created_at": "2025-10-04T20:00:00Z"
                }
            }
        ),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Бизнес-элемент не найден"
    },
    tags=['Администрирование']
)

business_element_destroy_schema = swagger_auto_schema(
    operation_id='business_elements_destroy',
    operation_summary='Удаление бизнес-элемента',
    operation_description='''
    Удаление существующего бизнес-элемента (только для Admin).

    **Внимание:** Удаление бизнес-элемента также удалит все связанные правила доступа.
    ''',
    responses={
        204: "Бизнес-элемент удален",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Бизнес-элемент не найден"
    },
    tags=['Администрирование']
)

