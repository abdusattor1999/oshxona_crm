from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from autoslug import AutoSlugField

class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=64, verbose_name="Telefon", unique=True)
    is_active = models.BooleanField(default=False, verbose_name='Activligi')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True, verbose_name='Activlashgan Vaqti')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def edit_phone(self, number):
        self.phone = number
        self.save()

    def __str__(self):
        return str(self.phone)

class Kitchen(models.Model):
    name = models.CharField(max_length=50, verbose_name="Oshxona nomi")
    slug = AutoSlugField(populate_from='name')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Foydalanuchi')
    image = models.ImageField(upload_to='images/kitchen-images/', verbose_name='Oshxona Logosi')
    description = models.TextField(verbose_name='Oshxona haqida malumot')
    status = models.BooleanField(default=True, verbose_name='Aktivlik holati')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50, verbose_name='Lavozim nomi')
    slug = AutoSlugField(populate_from='name')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, verbose_name='Oshxona')
    status = models.BooleanField(default=True , verbose_name="Aktivlik holati")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sanasi")

    def __str__(self):
        return self.name

    
class Worker(User):
    name = models.CharField(max_length=30, verbose_name='Ism')
    surname = models.CharField(max_length=30, verbose_name='Familiya')
    slug = AutoSlugField(populate_from='name', unique_with=('oshxona', 'created'))
    salary = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='Maosh (ixtiyoriy)')
    oshxona = models.ForeignKey(Kitchen, on_delete=models.CASCADE, verbose_name='Oshxona')
    position = models.ForeignKey(Position , on_delete=models.SET_NULL, null=True, verbose_name="Lavozimi")
    percentage = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ulush Foizda (ixtiyoriy)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return f"{self.name} {self.surname}".title()


