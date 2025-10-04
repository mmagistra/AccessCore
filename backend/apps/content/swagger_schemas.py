from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ProjectSerializer, TaskSerializer, ReportSerializer

# Общие ответы
unauthorized_response = openapi.Response(
    description="Требуется авторизация",
    examples={
        "application/json": {
            "error": "Требуется авторизация",
            "message": "Для доступа к этому ресурсу необходимо предоставить действительный JWT токен"
        }
    }
)

forbidden_response = openapi.Response(
    description="Недостаточно прав доступа",
    examples={
        "application/json": {
            "error": "Доступ запрещен",
            "message": "У вас нет разрешения для выполнения этого действия"
        }
    }
)

# Схемы для проектов
project_list_schema = swagger_auto_schema(
    operation_id='projects_list',
    operation_summary='Список проектов',
    operation_description='''
    Получение списка проектов в зависимости от роли пользователя:

    - **Admin**: видит все проекты
    - **Manager**: видит все проекты  
    - **User**: видит только свои проекты

    **Требует JWT авторизации**
    ''',
    responses={
        200: openapi.Response(
            description="Список проектов",
            schema=ProjectSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "title": "Проект разработки API",
                        "description": "Создание REST API для системы управления",
                        "status": "active",
                        "owner": {
                            "id": 1,
                            "username": "manager",
                            "first_name": "Менеджер"
                        },
                        "created_at": "2025-10-04T12:00:00Z"
                    }
                ]
            }
        ),
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Проекты']
)

project_create_schema = swagger_auto_schema(
    operation_id='projects_create',
    operation_summary='Создание проекта',
    operation_description='''
    Создание нового проекта. Аутентифицированный пользователь автоматически становится владельцем.

    **Права доступа:**
    - Admin: может создавать
    - Manager: может создавать
    - User: может создавать
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Название проекта',
                max_length=200,
                example='Проект разработки API'
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Описание проекта',
                example='Создание REST API для системы управления проектами'
            ),
            'status': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Статус проекта',
                default='active',
                example='active'
            )
        },
        required=['title', 'description']
    ),
    responses={
        201: openapi.Response(
            description="Проект создан",
            schema=ProjectSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Проект разработки API",
                    "description": "Создание REST API для системы управления проектами",
                    "status": "active",
                    "owner": {
                        "id": 2,
                        "username": "manager",
                        "first_name": "Менеджер",
                        "last_name": "Менеджеров"
                    },
                    "created_at": "2025-10-04T19:55:00Z"
                }
            }
        ),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Проекты']
)

project_retrieve_schema = swagger_auto_schema(
    operation_id='projects_retrieve',
    operation_summary='Получение проекта',
    operation_description='Получение конкретного проекта по ID',
    responses={
        200: openapi.Response(description="Данные проекта", schema=ProjectSerializer),
        404: "Проект не найден",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Проекты']
)

project_update_schema = swagger_auto_schema(
    operation_id='projects_update',
    operation_summary='Обновление проекта',
    operation_description='''
    Полное обновление проекта.

    **Права доступа:**
    - Admin: может редактировать все проекты
    - Manager: может редактировать все проекты
    - User: может редактировать только свои проекты
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, max_length=200),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['title', 'description']
    ),
    responses={
        200: openapi.Response(description="Проект обновлен", schema=ProjectSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Проект не найден"
    },
    tags=['Проекты']
)

project_destroy_schema = swagger_auto_schema(
    operation_id='projects_destroy',
    operation_summary='Удаление проекта',
    operation_description='''
    Удаление проекта.

    **Права доступа:**
    - Admin: может удалять все проекты
    - Manager: НЕ может удалять проекты
    - User: может удалять только свои проекты
    ''',
    responses={
        204: "Проект удален",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Проект не найден"
    },
    tags=['Проекты']
)

# Схемы для задач
task_list_schema = swagger_auto_schema(
    operation_id='tasks_list',
    operation_summary='Список задач',
    operation_description='''
    Получение списка задач в зависимости от роли пользователя:

    - **Admin**: видит все задачи
    - **Manager**: видит все задачи
    - **User**: видит только свои задачи
    ''',
    responses={
        200: openapi.Response(
            description="Список задач",
            schema=TaskSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "title": "Реализовать аутентификацию",
                        "description": "Создать систему JWT аутентификации",
                        "completed": False,
                        "assignee": {
                            "id": 2,
                            "username": "user",
                            "first_name": "Пользователь"
                        },
                        "created_at": "2025-10-04T14:00:00Z"
                    }
                ]
            }
        ),
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Задачи']
)

task_create_schema = swagger_auto_schema(
    operation_id='tasks_create',
    operation_summary='Создание задачи',
    operation_description='''
    Создание новой задачи. Аутентифицированный пользователь автоматически назначается исполнителем.
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Название задачи',
                max_length=200,
                example='Реализовать аутентификацию'
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Описание задачи',
                example='Создать систему JWT аутентификации с проверкой ролей'
            ),
            'completed': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='Статус выполнения',
                default=False,
                example=False
            )
        },
        required=['title']
    ),
    responses={
        201: openapi.Response(
            description="Задача создана",
            schema=TaskSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Реализовать аутентификацию",
                    "description": "Создать систему JWT аутентификации с проверкой ролей",
                    "completed": False,
                    "assignee": {
                        "id": 3,
                        "username": "user",
                        "first_name": "Пользователь"
                    },
                    "created_at": "2025-10-04T19:55:00Z"
                }
            }
        ),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Задачи']
)

task_update_schema = swagger_auto_schema(
    operation_id='tasks_update',
    operation_summary='Обновление задачи',
    operation_description='''
    Обновление задачи.

    **Права доступа:**
    - Admin: может редактировать все задачи
    - Manager: может редактировать только свои задачи
    - User: может редактировать только свои задачи
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, max_length=200),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        },
        required=['title']
    ),
    responses={
        200: openapi.Response(description="Задача обновлена", schema=TaskSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Задача не найдена"
    },
    tags=['Задачи']
)

task_destroy_schema = swagger_auto_schema(
    operation_id='tasks_destroy',
    operation_summary='Удаление задачи',
    operation_description='''
    Удаление задачи.

    **Права доступа:**
    - Admin: может удалять все задачи
    - Manager: может удалять только свои задачи  
    - User: может удалять только свои задачи
    ''',
    responses={
        204: "Задача удалена",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Задача не найдена"
    },
    tags=['Задачи']
)

# Схемы для отчетов
report_list_schema = swagger_auto_schema(
    operation_id='reports_list',
    operation_summary='Список отчетов',
    operation_description='''
    Получение списка отчетов в зависимости от роли пользователя:

    - **Admin**: видит все отчеты
    - **Manager**: видит все отчеты
    - **User**: видит только свои отчеты
    ''',
    responses={
        200: openapi.Response(
            description="Список отчетов",
            schema=ReportSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "title": "Отчет о прогрессе проекта",
                        "content": "Детальный отчет о выполнении задач...",
                        "is_published": True,
                        "author": {
                            "id": 3,
                            "username": "manager",
                            "first_name": "Менеджер"
                        },
                        "created_at": "2025-10-04T16:00:00Z"
                    }
                ]
            }
        ),
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Отчеты']
)

report_create_schema = swagger_auto_schema(
    operation_id='reports_create',
    operation_summary='Создание отчета',
    operation_description='''
    Создание нового отчета. Аутентифицированный пользователь автоматически становится автором.

    **Права доступа:**
    - Admin: может создавать
    - Manager: может создавать
    - User: НЕ может создавать отчеты
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Название отчета',
                max_length=200,
                example='Отчет о прогрессе проекта'
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Содержание отчета',
                example='Детальный отчет о выполнении задач за текущий период...'
            ),
            'is_published': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='Опубликован ли отчет',
                default=False,
                example=True
            )
        },
        required=['title', 'content']
    ),
    responses={
        201: openapi.Response(
            description="Отчет создан",
            schema=ReportSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Отчет о прогрессе проекта",
                    "content": "Детальный отчет о выполнении задач за текущий период...",
                    "is_published": True,
                    "author": {
                        "id": 2,
                        "username": "manager",
                        "first_name": "Менеджер"
                    },
                    "created_at": "2025-10-04T19:55:00Z"
                }
            }
        ),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Отчеты']
)

report_update_schema = swagger_auto_schema(
    operation_id='reports_update',
    operation_summary='Обновление отчета',
    operation_description='''
    Обновление отчета.

    **Права доступа:**
    - Admin: может редактировать все отчеты
    - Manager: может редактировать только свои отчеты
    - User: НЕ может редактировать отчеты
    ''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, max_length=200),
            'content': openapi.Schema(type=openapi.TYPE_STRING),
            'is_published': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        },
        required=['title', 'content']
    ),
    responses={
        200: openapi.Response(description="Отчет обновлен", schema=ReportSerializer),
        400: "Ошибки валидации",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Отчет не найден"
    },
    tags=['Отчеты']
)

report_destroy_schema = swagger_auto_schema(
    operation_id='reports_destroy',
    operation_summary='Удаление отчета',
    operation_description='''
    Удаление отчета.

    **Права доступа:**
    - Admin: может удалять все отчеты
    - Manager: НЕ может удалять отчеты
    - User: НЕ может удалять отчеты
    ''',
    responses={
        204: "Отчет удален",
        401: unauthorized_response,
        403: forbidden_response,
        404: "Отчет не найден"
    },
    tags=['Отчеты']
)

project_retrieve_schema = swagger_auto_schema(
    operation_id='projects_retrieve',
    operation_summary='Получение проекта по ID',
    operation_description='''
    Получение конкретного проекта по его ID.

    **Права доступа:**
    - Admin: может получить любой проект
    - Manager: может получить любой проект
    - User: может получить только свои проекты
    ''',
    responses={
        200: openapi.Response(
            description="Данные проекта",
            schema=ProjectSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Проект разработки API",
                    "description": "Создание REST API для системы управления проектами",
                    "status": "active",
                    "owner": {
                        "id": 2,
                        "username": "manager",
                        "first_name": "Менеджер",
                        "last_name": "Менеджеров"
                    },
                    "created_at": "2025-10-04T19:55:00Z"
                }
            }
        ),
        404: "Проект не найден",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Проекты']
)

task_retrieve_schema = swagger_auto_schema(
    operation_id='tasks_retrieve',
    operation_summary='Получение задачи по ID',
    operation_description='''
    Получение конкретной задачи по её ID.

    **Права доступа:**
    - Admin: может получить любую задачу
    - Manager: может получить любую задачу
    - User: может получить только свои задачи
    ''',
    responses={
        200: openapi.Response(
            description="Данные задачи",
            schema=TaskSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Реализовать аутентификацию",
                    "description": "Создать систему JWT аутентификации с проверкой ролей",
                    "completed": False,
                    "assignee": {
                        "id": 3,
                        "username": "user",
                        "first_name": "Пользователь"
                    },
                    "created_at": "2025-10-04T19:55:00Z"
                }
            }
        ),
        404: "Задача не найдена",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Задачи']
)

report_retrieve_schema = swagger_auto_schema(
    operation_id='reports_retrieve',
    operation_summary='Получение отчета по ID',
    operation_description='''
    Получение конкретного отчета по его ID.

    **Права доступа:**
    - Admin: может получить любой отчет
    - Manager: может получить любой отчет
    - User: может получить только свои отчеты
    ''',
    responses={
        200: openapi.Response(
            description="Данные отчета",
            schema=ReportSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Отчет о прогрессе проекта",
                    "content": "Детальный отчет о выполнении задач за текущий период...",
                    "is_published": True,
                    "author": {
                        "id": 2,
                        "username": "manager",
                        "first_name": "Менеджер"
                    },
                    "created_at": "2025-10-04T19:55:00Z"
                }
            }
        ),
        404: "Отчет не найден",
        401: unauthorized_response,
        403: forbidden_response
    },
    tags=['Отчеты']
)

