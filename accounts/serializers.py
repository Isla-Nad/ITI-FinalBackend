from requests import request
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import re

from accounts.models import Cases, Certificates, UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'confirm_password',
                  'is_doctor', 'phone', 'clinic')
        extra_kwargs = {
            'password': {'write_only': True},
            'clinic': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match.'})

        email = data.get('email', '')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError(
                {'email': 'Invalid email address.'})

        phone = data.get('phone', '')

        if not re.match(r"^01[0-9]{9}$", phone):
            raise serializers.ValidationError(
                {'phone': 'Invalid Egyptian phone number format.'})

        if data.get('is_doctor') and not data.get('clinic'):
            raise serializers.ValidationError(
                {'clinic': 'Clinic is required for doctors.'})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(read_only=True)

    def check_user(self, clean_data):
        user = authenticate(
            email=clean_data['email'], password=clean_data['password'])
        if not user:
            raise serializers.ValidationError(
                {'message': 'email or password is incorrect'})
        return user


class UserCertificatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = '__all__'


class UserCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cases
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["info", "bio", "profile_picture", "contact"]


class UserProfileSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["info", "bio", "contact"]


class UserSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'clinic']

    def validate(self, data):
        phone = data.get('phone', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        if not re.match(r"^01[0-9]{9}$", phone):
            raise serializers.ValidationError(
                {'phone': 'Invalid Egyptian phone number format.'})

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", first_name):
            raise serializers.ValidationError(
                {'first_name': 'Please use only alphanumeric characters, starting with a letter or underscore.'})

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", last_name):
            raise serializers.ValidationError(
                {'last_name': 'Please use only alphanumeric characters, starting with a letter or underscore.'})

        if data.get('first_name') is None:
            raise serializers.ValidationError(
                {'first_name': 'This field cannot be null.'})

        if data.get('last_name') is None:
            raise serializers.ValidationError(
                {'last_name': 'This field cannot be null.'})

        return data


class UserPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_picture"]
