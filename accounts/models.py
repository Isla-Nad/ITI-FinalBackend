from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_doctor(self, email, clinic, password=None, **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        if extra_fields.get('is_doctor') is not True:
            raise ValueError(_('Doctors must have is_doctor=True.'))
        return self.create_user(email, password, clinic=clinic, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True,)
    is_doctor = models.BooleanField(_('doctor status'), default=False)
    phone = models.CharField(
        max_length=15, help_text="Enter an Egyptian phone number (e.g., +201234567890)")
    clinic = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
