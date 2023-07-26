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
        return True

    def post(self, request):
        serializer = ChangePhoneSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(phone=serializer.validated_data['phone'])
            if user.exists():
                user = user.last()
                phone = serializer.validated_data['new_phone']
                self.validate_phone_number(phone)
                user.phone = phone
                user.save()
                return Response({"success": True, 'message': "Telefon Raqam yangiandi"}, status=status.HTTP_200_OK)
            else:
                return Response({"success":False, "message":"Berilgan raqamdagi foydalanuvchi topilmadi"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = IsAuthenticated,
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(phone=serializer.data.get('phone', ''))
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"success": False, "message": "Eski parol noto'g'ri kiritildi. Tekshirib qaytadan kiriting !"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'success': True,
                'message': 'Parol yangilash muvaffaqiyatli bajarildi',
                'status': status.HTTP_200_OK,
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# =============================================================================================================
class KitchenApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = KitchenEditSerializer
    queryset = Kitchen.objects.all()

    

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response({"success":True, "message":"Oshxona malumotlari yangilandi"})


    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Oshxona o'chirildi"})

# =============================================================================================================

class WorkerCreateView(APIView):
    serializer_class = WorkerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        worker = Worker.objects.create_user(**serializer.validated_data)
        worker.save()
        return Response({'success':True, 'message':"Ishchi yaratish muvaffaqiyatli amalga oshirildi."})
    

class WorkerAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkerEditSerializer
    queryset = Worker.objects.all()
    

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response({"success":True, "message":"Profil malumotlari yangilandi"})


    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Profil o'chirildi"})
