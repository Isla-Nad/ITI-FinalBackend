from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer, UserSerializer
from clinics.models import Clinic, Cases, ClinicImages
from clinics.serializers import ClinicSerializer, CaseSerializer, ClinicImageSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        clinic = Clinic.objects.create(name=request.data['name'],
                                       desc=request.data['desc'],
                                       image=request.data['image'],
                                       address=request.data['address'],
                                       phone=request.data['phone']
                                       )
        clinic.save()
        return Response({'clinic': ClinicSerializer(clinic).data})
    elif request.method == 'GET':
        clinics = Clinic.get_all_clinics()
        serialized_clinics = []
        for cln in clinics:
            serialized_clinics.append(ClinicSerializer(cln).data)

        return Response({"clinics": serialized_clinics})


@api_view(['GET'])
def show(request, id):
    clinic = Clinic.objects.get(id=id)
    cases_for_clinic = Cases.objects.filter(clinic_id=id)
    images_for_clinic = ClinicImages.objects.filter(clinic_id=id)
    doctors_for_clinic = clinic.user_set.filter(is_doctor=True)

    clinic_data = ClinicSerializer(clinic).data
    cases_data = CaseSerializer(cases_for_clinic, many=True).data
    images_data = ClinicImageSerializer(images_for_clinic, many=True).data
    profiles = UserProfile.objects.filter(user__in=doctors_for_clinic)

    doctor_data = []
    for doctor in doctors_for_clinic:
        user_serializer = UserSerializer(doctor)
        profile = profiles.filter(user=doctor).first()
        profile_serializer = UserProfileSerializer(profile)
        combined_data = {**user_serializer.data, **profile_serializer.data}
        doctor_data.append(combined_data)

    return Response({'clinic': clinic_data, 'cases': cases_data, 'images': images_data, 'doctors': doctor_data})


@api_view(['POST'])
def delete(request, id):
    clinic = Clinic.objects.get(id=id)
    clinic.delete()
    return Response({"message": "Clinic deleted successfully"})


@api_view(['POST'])
def create_case(request):
    serializer = CaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_clinic_image(request):
    serializer = ClinicImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_clinics(request):
    search_query = request.GET.get('search_query', '')
    clinics = Clinic.objects.all()

    if search_query:
        clinics = clinics.filter(name__icontains=search_query)

    serializer = ClinicSerializer(clinics, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
