from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.serializers import UserCasesSerializer, UserCertificatesSerializer, UserPicSerializer, UserProfileSerializer, UserProfileSerializerEdit, UserSerializer, UserSerializerEdit
from accounts.models import Cases, Certificates, User, UserProfile
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser

from clinics.models import Clinic
from clinics.serializers import ClinicSerializer


class UserSignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=request.data['email'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLogin(APIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = (SessionAuthentication,)

#     def post(self, request):
#         data = request.data
#         email = data.get('email', '').strip()
#         if not email:
#             raise ValidationError('An email is needed')

#         password = data.get('password', '').strip()
#         if not password:
#             raise ValidationError('A password is needed')

#         serializer = UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.check_user(data)
#             login(request, user)
#             print(request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)


# class UserLogout(APIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = ()

#     def post(self, request):
#         logout(request)
#         return Response(status=status.HTTP_200_OK)


# class UserView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)

#     def get(self, request):
#         print(request.user)
#         serializer = UserSerializer(request.user)
#         return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        print(user)
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    print(request.user)
    serializer = UserSerializer(request.user)
    return Response({'user': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_profile(request, id):
    user = get_object_or_404(User, id=id)
    profile = UserProfile.objects.get(id=user.id)

    clinic_data = {}
    if user.clinic:
        clinic = get_object_or_404(Clinic, id=user.clinic.id)
        clinic_serializer = ClinicSerializer(clinic)
        clinic_data = clinic_serializer.data

    user_serializer = UserSerializer(user)
    profile_serializer = UserProfileSerializer(profile)

    combined_serializer = {
        **user_serializer.data,
        **profile_serializer.data,
        'clinic_data': clinic_data,
    }
    return Response(combined_serializer, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, id=user.id)
    profile_serializer = UserProfileSerializerEdit(
        user_profile, data=request.data, partial=True)
    user_serializer = UserSerializerEdit(
        user, data=request.data, partial=True)
    if user_serializer.is_valid() and profile_serializer.is_valid():
        user_serializer.save()
        profile_serializer.save()
        combined_serializer = {
            **user_serializer.data,
            **profile_serializer.data
        }
        combined_errors = {
            **user_serializer.errors,
            **profile_serializer.errors
        }
        return Response(combined_serializer, status=status.HTTP_200_OK)
    return Response(combined_errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def edit_profile_pic(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, id=user.id)
    serializer = UserPicSerializer(
        user_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_pic(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user.id)

    if user_profile.profile_picture:
        user_profile.profile_picture.delete()
        user_profile.profile_picture = None
        user_profile.save()
        serializer = UserPicSerializer(
            user_profile,  partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("No profile picture to delete.", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_case(request):
    serializer = UserCasesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cases(request, id):
    cases = Cases.objects.filter(user=id)
    serializer = UserCasesSerializer(cases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_case(request, id):
    user = request.user
    case = get_object_or_404(Cases, id=id, user=user.id)
    case.delete()
    return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_certificate(request):
    serializer = UserCertificatesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_certificates(request, id):
    certificates = Certificates.objects.filter(user=id)
    serializer = UserCertificatesSerializer(certificates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_certificate(request, id):
    user = request.user
    certificate = get_object_or_404(Certificates, id=id, user=user.id)
    certificate.delete()
    return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def search_doctors(request):
    search_query = request.GET.get('search_query', '')
    doctors = User.objects.filter(is_doctor=True)

    if search_query:
        doctors = doctors.filter(first_name__icontains=search_query)

    profiles = UserProfile.objects.filter(user__in=doctors)

    doctor_data = []
    for doctor in doctors:
        user_serializer = UserSerializer(doctor)
        profile = profiles.filter(user=doctor).first()
        profile_serializer = UserProfileSerializer(profile)
        combined_data = {**user_serializer.data, **profile_serializer.data}
        doctor_data.append(combined_data)

    return Response(doctor_data)
