from rest_framework import serializers
from .models import Project, Task, Report
from apps.custom_auth.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        user = self.context.get('user')
        if user:
            validated_data['owner'] = user
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['assignee', 'created_at']

    def create(self, validated_data):
        assignee = self.context.get('user')
        if assignee:
            validated_data['assignee'] = assignee
        return super().create(validated_data)


class ReportSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ['author', 'created_at']

    def create(self, validated_data):
        author = self.context.get('user')
        if author:
            validated_data['author'] = author
        return super().create(validated_data)
