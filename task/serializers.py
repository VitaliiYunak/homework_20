from rest_framework import serializers
from datetime import date
from django.contrib.auth.models import User


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    due_date = serializers.DateField()

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializerUser(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    due_date = serializers.DateField()
    user = UserSerializer()

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Дата виконання не може бути в минулому.")
        return value