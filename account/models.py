from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from feed.models import *


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('You need to use an email to log in as a user!')
        if not username:
            raise ValueError('Please input a username')
    
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom General User Model
class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.TimeField(auto_now_add=True,
                                   verbose_name='date joined')
    last_login = models.DateField(auto_now=True, verbose_name='last seen')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Sets the login field to email instead of username
    # & makes the username required, as it cant be set in the model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True

    def number_of_posts(self):
        return Post.objects.filter(author=self).count()

    def number_of_comments(self):
        return Comment.objects.filter(commenter=self).count()

    def number_of_likes(self):
        queryset = Post.objects.filter(listed=True)
        count = 0
        for post in queryset:
            if post.likes.filter(id=self.id).exists():
                count = count+1
        return count

    def number_of_dislikes(self):
        queryset = Post.objects.filter(listed=True)
        count = 0
        for post in queryset:
            if post.dislikes.filter(id=self.id).exists():
                count = count+1
        return count
