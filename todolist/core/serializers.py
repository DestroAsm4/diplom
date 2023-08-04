from rest_framework import serializers, exceptions
from django.contrib.auth.hashers import make_password

from core.models import User
from todolist.fields import PasswordField

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField()
    password_repeat = PasswordField(validate=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise exceptions.ValidationError('Passwords must match')
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = PasswordField(validate=False)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(validate=False)
    new_password = PasswordField()

    def validate_old_password(self, old_password: str) -> str:
        request = self.context['request']

        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated

        if not request.user.check_password(old_password):
            raise exceptions.ValidationError('Current password is incorrect')

        return old_password
