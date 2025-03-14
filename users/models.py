from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.choices import ROLES
from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=255, choices=ROLES, default=ROLES.EMPLOYEE)
    contacts = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    position = models.ForeignKey('users.Position', on_delete=models.SET_NULL, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Position(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.IntegerField()

    def __str__(self):
        return self.name
