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

# class UserProfileSerializer(serializers.ModelSerializer):
#     certificates = UserCertificatesSerializer(many=True, read_only=True)
#     cases = UserCasesSerializer(many=True, read_only=True)
#     uploaded_certificates = serializers.ListField(
#         child=serializers.ImageField(allow_empty_file=False, use_url=False),
#         write_only=True
#     )
#     uploaded_cases = serializers.ListField(
#         child=serializers.ImageField(allow_empty_file=False, use_url=False),
#         write_only=True
#     )

#     class Meta:
#         model = UserProfile
#         fields = ["info", "bio", "profile_picture", "contact", "certificates", "cases",
#                   "uploaded_certificates", "uploaded_cases"]

#     def create(self, validated_data):
#         uploaded_certificates = validated_data.pop("uploaded_certificates")
#         uploaded_cases = validated_data.pop("uploaded_cases")
#         profile = UserProfile.objects.create(**validated_data)

#         for image in uploaded_certificates:
#             Certificates.objects.create(profile=profile, certificates=image)
#         for image in uploaded_cases:
#             Cases.objects.create(profile=profile, cases=image)
#         return profile
