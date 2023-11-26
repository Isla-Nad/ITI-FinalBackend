from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from clinics.models import Clinic


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
    clinic = models.ForeignKey(
        Clinic, null=True, blank=True, on_delete=models.CASCADE)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='accounts/images/', blank=True, null=True)
    contact = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(
                user=instance, bio="This is the default bio.")

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class Certificates(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    certificate = models.ImageField(
        upload_to='accounts/images/', blank=True, null=True)

    def __str__(self):
        return f"{self.image}"


class Cases(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    case = models.ImageField(
        upload_to='accounts/images/', blank=True, null=True)

    def __str__(self):
        return f"{self.image}"
