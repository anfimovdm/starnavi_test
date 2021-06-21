from django.contrib.auth.models import (
    User,
)

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Post,
)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'token',
        )

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'total_likes',
            'owner',
            'date_created',
        )


class AnalyticSerializer(serializers.Serializer):
    day = serializers.DateField(read_only=True)
    count = serializers.IntegerField(read_only=True)


class UserActivitySerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M',
        read_only=True,
    )
    last_request = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M',
        read_only=True,
    )
