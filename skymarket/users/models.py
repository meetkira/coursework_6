from typing import Any, List, Tuple

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


def get_choices(constants_class: Any) -> List[Tuple[str, str]]:
    return [
        (value, value)
        for key, value in vars(constants_class).items()
        if not key.startswith('__')
    ]

class UserRoles:
    USER = "user"
    ADMIN = "admin"


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(max_length=9, default=UserRoles.USER, choices=get_choices(UserRoles))
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role",]

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN  #

    @property
    def is_user(self):
        return self.role == UserRoles.USER
