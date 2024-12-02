from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import string
import random

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Телефонный номер обязателен')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_unusable_password()  # Если вы не используете пароли
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    activated_invite_code = models.CharField(max_length=6, blank=True, null=True)
    referrals = models.ManyToManyField('self', symmetrical=False, related_name='referred_by', blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super(User, self).save(*args, **kwargs)

    def generate_invite_code(self):
        import string, random
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
