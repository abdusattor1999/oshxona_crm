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
        write_only_fields = 'password',

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


class ChangePasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    class Meta:
        model = User

    def validate(self, attrs): 
        katta = False
        kichik = False
        belgi = False
        raqam = False

        new_pass = attrs['new_password']
        belgilar = ("." , "_" , "*" , "-" , "$" , "#")
        for i in new_pass:
            if 64 < ord(i) < 91:
                katta = True
            elif 96 < ord(i) < 123:
                kichik = True
            elif i in belgilar:
                belgi = True
            elif 47 < ord(i) < 58:
                raqam = True
        if len(new_pass) < 8:
            raise serializers.ValidationError({"success":False, "message":"Parol 8 ta raqamdan kam bo'lmasligi kerak"})
        elif katta+kichik+belgi+raqam < 2:
            raise serializers.ValidationError({"success":False, "message":f"Parol xavfsizlik talabiga javob bermaydi katta va kichik harflar yoki {belgilar} belgilaridan foydalaning"})

        return attrs
    

# ============= User ends  ->  Oshxona starts =============================================

class KitchenEditSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Kitchen
        fields = 'id', 'name','user', 'image', 'description', 'status', 'created'
        read_only_fields = 'id','user','created'


# ============= Oshxona ends  ->  Worker starts ===========================================
class WorkerSerializer(serializers.ModelSerializer):
    oshxona = KitchenEditSerializer()
    class Meta:
        model = Worker
        fields = 'id', "name", "surname", "phone", "password", "salary", "oshxona", "position", "percentage"
        read_only_fields = 'id',
        write_only_fields = 'password',

    def create(self, validated_data):
        worker = Worker.objects.create_user(**validated_data)
        return worker
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class WorkerEditSerializer(serializers.ModelSerializer):
    oshxona = KitchenEditSerializer()
    class Meta:
        model = Worker
        fields = 'id', "name", "surname", "phone", "salary", "oshxona", "position", "percentage"
        read_only_fields = 'id',