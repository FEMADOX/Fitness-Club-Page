from typing import Any

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[]
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, Any]) -> User:
        user = User(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[]
        model = User
        fields = ["username", "password"]

    @classmethod
    def get_token(cls, user: User) -> dict[str, Any]:
        token = super().get_token(user)  # type: ignore[]
        token["username"] = user.username
        token["fullname"] = f"{user.first_name} {user.last_name}"

        return token


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs: dict) -> dict[str, Any]:
        refresh = attrs["refresh"]

        token = RefreshToken(refresh)
        return {"access": str(token.access_token)}
