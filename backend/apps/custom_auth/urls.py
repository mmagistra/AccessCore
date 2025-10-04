from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    RoleViewSet,
    AccessRuleViewSet,
    BusinessElementViewSet, DeleteAccountView,
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'access-rules', AccessRuleViewSet, basename='accessrule')
router.register(r'business-elements', BusinessElementViewSet, basename='businesselement')


app_name = 'custom_auth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('', include(router.urls)),
]
