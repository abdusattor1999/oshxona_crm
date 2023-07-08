from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=64, verbose_name="Telefon", unique=True)
    activated_date = models.DateTimeField(blank=True, null=True, verbose_name='Activlashgan Vaqti')
    is_seller = models.BooleanField(default=False, verbose_name="Sotuvchi holati")
    is_active = models.BooleanField(default=False, verbose_name='Activligi')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def edit_phone(self, number):
        self.phone = number
        self.save()


    def __str__(self):
        return str(self.phone)
