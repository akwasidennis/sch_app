from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where index_number is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, index_number, password, **extra_fields):
        """
        Create and save a User with the given index_number and password.
        """
        if not index_number:
            raise ValueError(_('The Index number must be set'))
        
        email = self.normalize_email(extra_fields.get('email'))
        user = self.model(index_number=index_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, index_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given index_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('last_login', True)
        extra_fields.setdefault('date_joined', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Admin must have is_admin=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(index_number, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email address'), blank=True)
    index_number = models.CharField(_('index number'), max_length=100, unique=True)
    course = models.CharField(_('course'), max_length=100, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'index_number'
    REQUIRED_FIELDS = ['course', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.index_number

