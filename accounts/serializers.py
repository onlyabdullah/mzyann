from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_auth import serializers as auth_serializers
from rest_auth.registration import serializers as register_serializer

from .models import (
    Profile, PriceList, SocialLink
)

from .validators import name_validator

UserModel = get_user_model()

class LoginSerializer(auth_serializers.LoginSerializer):
    """
    Serializer inherits from rest-auth LoginSerializer
    to customize some features
    """
    username = None
    email = serializers.EmailField(required=True, allow_blank=False)


class RegisterSerializer(register_serializer.RegisterSerializer):
    """
    Serializer inherits from rest-auth RegisterSerializer
    to customize some features
    """
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    username = None
    email = serializers.EmailField(required=True, allow_blank=False)
    first_name = serializers.CharField(min_length=3, max_length=50, required=True, validators=[name_validator])
    last_name = serializers.CharField(min_length=3, max_length=50, required=True, validators=[name_validator])
    birthday = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'birthday': self.validated_data.get('birthday', ''),
            'gender': self.validated_data.get('gender', ''),
        }

    def custom_signup(self, request, user):
        user.birthday = self.cleaned_data.get('birthday', '')
        user.gender = self.cleaned_data.get('gender', '')
        user.save()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'email', 'first_name', 'last_name', 'birthday', 'gender')


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile Model
    """
    pass
