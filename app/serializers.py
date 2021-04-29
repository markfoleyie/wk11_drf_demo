from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class UserMeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["name", "email", "is_admin"]

    def get_name(self, obj):
        return obj.get_full_name()

    def get_is_admin(self, obj):
        return obj.is_staff


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_admin = serializers.BooleanField()

