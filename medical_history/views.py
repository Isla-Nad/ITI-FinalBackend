from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from medical_history.models import MedicalHistory
from medical_history.serializers import MedicalHistorySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medical_history(request, id):
    doctor = get_object_or_404(User, id=id)
    medical_history = MedicalHistory.objects.filter(
        doctor=doctor).order_by('-created_at')
    serializer = MedicalHistorySerializer(medical_history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def medical_history_create(request):
    serializer = MedicalHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(doctor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def medical_history_edit(request, id):
    medical_history = get_object_or_404(
        MedicalHistory, id=id, doctor=request.user)
    serializer = MedicalHistorySerializer(medical_history, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def medical_history_delete(request, id):
    medical_history = get_object_or_404(
        MedicalHistory, id=id, doctor=request.user)
    medical_history.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
