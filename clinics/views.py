from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from clinics.models import Clinic,Cases
from clinics.serializers import ClinicSerializer,CaseSerializer
from rest_framework import status

@api_view(['GET','POST'])
def index (request):
    if request.method == 'POST':
        clinic = Clinic.objects.create(name=request.data['name'], 
                                        desc=request.data['desc'],
                                        image=request.data['image'],
                                        address=request.data['address']
                                        )
        clinic.save()
        return Response({'clinic':ClinicSerializer(clinic).data})
    elif request.method == 'GET':
        clinics = Clinic.get_all_clinics()
        serialized_clinics = []
        for cln in clinics:
            serialized_clinics.append(ClinicSerializer(cln).data)
            
        return Response({"clinics":serialized_clinics})
    
@api_view(['GET'])   
def show(request,id):
    clinic = Clinic.objects.get(id=id)
    cases_for_clinic = Cases.objects.filter(clinic_id=id)
    
    # Serialize the clinic and cases queryset as dictionaries
    clinic_data = ClinicSerializer(clinic).data
    cases_data = CaseSerializer(cases_for_clinic, many=True).data

    return Response({'clinic': clinic_data, 'cases': cases_data})

@api_view(['POST'])   
def delete(request,id):
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