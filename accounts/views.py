from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
import re
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status


class SignupView(APIView):
    permission_classes = AllowAny,
    serializer_class = UserSerializer

    def validate_phone_number(self, phone):
        pattern = re.compile(
            r"^[\+]?[(]?[9]{2}?[8]{1}[)]?[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{7}$")
        if not pattern.match(phone):
            data = {
                "success": False,
                "message": "Telefon raqami to'g'ri kiritilmadi."
            }
            raise ValidationError(data)
        return True
    
    def validate_password(self, password):
        upp = False
        low = False
        for i in password:
            if i.isupper():
                upp = True
            if i.islower():
                low = True
        if len(password) > 7 and upp + low == 2:
            return True
        else:
            data = {
                "success": False,
                "message": "Parol uzunligi eng kami 8 ta belgi , katta kichik lotin harflaridan foydalaning"
            }
            raise ValidationError(data)

    def post(self, request, *args, **kwargs):
        phone = self.request.data.get('phone', None)
        password = self.request.data.get('password', None)
        self.validate_phone_number(phone=phone)
        self.validate_password(password=password)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        user.is_active = True
        user.save()

        data = {
            'success': True,
            'message': "Ro'yxatdan o'tish muvaffaqiyatli."
        }
        return Response(data)

from rest_framework_simplejwt.views import TokenViewBase

class LoginView(TokenViewBase):
    serializer_class = LoginSerializer


class LoguotView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = IsAuthenticated,

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success": True, "message": "Tizimdan chiqish muvaffaqiyatli !"}, status=status.HTTP_204_NO_CONTENT)


class ChangePhoneView(APIView):
    permission_classes = IsAuthenticated,
    serializer_class = ChangePhoneSerializer

    def validate_phone_number(self, phone):
        pattern = re.compile(
            r"^[\+]?[(]?[9]{2}?[8]{1}[)]?[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{7}$")
        if not pattern.match(phone):
            data = {
                "success": False,
                "message": "Yangi telefon raqami to'g'ri kiritilmadi."
            }
            raise ValidationError(data)
        print('Validatsiya Muvaffaqiyatli !')
        return True

    def patch(self, request):
        serializer = ChangePhoneSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            phone = serializer.validated_data['new_phone']
            self.validate_phone_number(phone)
            user.edit_phone()
            return Response({"success": True, 'message': "Telefon Raqam yangiandi"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================================================

class WorkerCreateView(APIView):
    serializer_class = WorkerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # worker = Worker.objects.create_user(**serializer.validated_data)
        # worker.save()
        return Response({'success':True, 'message':"Ishchi yaratish muvaffaqiyatli amalga oshirildi."})
    
