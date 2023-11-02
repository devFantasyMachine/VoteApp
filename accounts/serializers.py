from django.contrib.auth.hashers import check_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize User model.
    """

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True},
                        'user_permissions': {"write_only": True},
                        'groups': {"write_only": True},
                        'is_superuser': {"write_only": True},
                        'is_staff': {"write_only": True},
                        'last_login': {"write_only": True},
                        'date_joined': {"write_only": True}}

        write_only_fields = ['password']
        read_only_fields = ['created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = User
        fields = ("id",  "username",  "ip", "mat", "device_id", "user_agent", "password")
        extra_kwargs = {"password": {"read_only": True}, "device_id": {"read_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)






class UserLoginSerializer(serializers.Serializer):
    """
        Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        try:

            password = data["password"]
            email = data["email"]
            user = User.objects.get(email=email)

            if not check_password(str(password), user.password):
                print("invalid pass")
                user = None

        except Exception:
            raise serializers.ValidationError("Incorrect Credentials")

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UpdateUserSerializer(UserSerializer):
    """
        Serializer class to serialize update user request
    """

    class Meta:
        model = User
        fields = ("user_agent", "name", "ip", "device_hash")
