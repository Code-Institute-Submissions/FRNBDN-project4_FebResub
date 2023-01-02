from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Custom General User Model
class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True, required=True)
    date_joined = models.TimeField(auto_now_add=True,
                                   verbose_name='date joined')
    last_login = models.DateField(auto_now=True, verbose_name='last seen')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Sets the login field to email instead of username
    # & makes the username required
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True