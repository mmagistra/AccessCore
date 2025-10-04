from django.db import models
import bcrypt
import jwt
from django.conf import settings
from datetime import datetime, timedelta


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    roles = models.ManyToManyField(Role, related_name='users')

    def set_password(self, raw_password):
        """Хеширует пароль с помощью bcrypt"""
        self.password_hash = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """Проверяет пароль"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_jwt_token(self):
        """Генерирует JWT токен для пользователя"""
        payload = {
            'email': self.email,
            'exp': datetime.now() + timedelta(hours=settings.JWT_TOKEN_LIFETIME_HOURS)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def __str__(self):
        return f"user {self.email}"


class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    # CRUD
    create_permission = models.BooleanField(default=False)

    read_own_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)

    update_own_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)

    delete_own_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['role', 'element']
