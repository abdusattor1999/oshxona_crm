from .models import *
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions

#  ====================== User starts =====================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'phone', 'password')

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def validate_user(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        return {}
    
    def validate(self, attrs):
        data = self.validate_user(attrs=attrs)
        refresh = self.get_token(self.user)

        data['id'] = str(self.user.id)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token':{
        "success":False,"message":"No'tog'ri token kiritildi" 
        },
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


class DeleteUserSerilizer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ("__all__")


class ChangePhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    new_phone = serializers.CharField(max_length=13)

# =========================== User ends ==============================================

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "name", "surname", "phone", "password", "salary", "oshxona", "position", "percentage"


    def create(self, validated_data):
        worker = Worker.objects.create_user(**validated_data)
        return worker