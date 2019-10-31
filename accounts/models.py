from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from allauth.account.signals import user_signed_up

from .validators import name_validator

class UserManager(BaseUserManager):
    """
    Custom user model to create users without username.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model inherits from Django AbstractUser Model
    edits:
        -Remove username field.
        -Make email unique and required.
        -Add birthday and gender fields.
        -Edit first_name and last_name fields.
    """

    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female'))
    )

    username = None
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, validators=[name_validator], blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, validators=[name_validator], blank=True)
    gender = models.CharField(_('Gender'), max_length=6, choices=GENDER_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    objects = UserManager()


    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return "{email}".format(email=self.email)

@receiver(user_signed_up)
def complete_social_signup(request, user, sociallogin=None, *args, **kwargs):
    if sociallogin:
        if sociallogin.account.provider == 'facebook':
            user.gender = sociallogin.account.extra_data.get('gender')
            user.save()
