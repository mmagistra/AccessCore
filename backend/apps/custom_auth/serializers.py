from rest_framework import serializers
from .models import CustomUser

from rest_framework import serializers
from .models import CustomUser, Role, AccessRule, BusinessElement


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class AccessRuleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    element = BusinessElementSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True, required=False)
    element_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = AccessRule
        fields = [
            'id', 'role', 'element', 'role_id', 'element_id',
            'create_permission', 'read_own_permission', 'read_all_permission',
            'update_own_permission', 'update_all_permission',
            'delete_own_permission', 'delete_all_permission', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        role_id = validated_data.pop('role_id', None)
        element_id = validated_data.pop('element_id', None)

        if role_id:
            validated_data['role_id'] = role_id
        if element_id:
            validated_data['element_id'] = element_id

        return super().create(validated_data)

    def update(self, instance, validated_data):
        role_id = validated_data.pop('role_id', None)
        element_id = validated_data.pop('element_id', None)

        if role_id:
            validated_data['role_id'] = role_id
        if element_id:
            validated_data['element_id'] = element_id

        return super().update(instance, validated_data)



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'password', 'password_confirm')

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'middle_name', 'created_at')
