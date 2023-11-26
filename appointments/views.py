from accounts.models import User
from accounts.serializers import UserSerializer
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat


@api_view(['GET'])
def appointments_get(request, id):
    doctor = get_object_or_404(User, id=id)
    appointments = Appointment.objects.filter(
        doctor=doctor).order_by('appointment_date', 'start_time')
    grouped_appointments = {}

    for appointment in appointments:
        appointment_date = appointment.appointment_date
        if appointment_date not in grouped_appointments:
            grouped_appointments[appointment_date] = []
        grouped_appointments[appointment_date].append(appointment)

    data = []

    for appointment_date, appointments in grouped_appointments.items():
        doctor_data = UserSerializer(appointments[0].doctor).data
        patient_data = UserSerializer(
            appointments[0].patient).data if appointments[0].patient else None
        appointment_data = AppointmentSerializer(appointments, many=True).data

        data.append({
            'appointment_date': appointment_date,
            'doctor': doctor_data,
            'patient': patient_data,
            'appointments': appointment_data
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def appointment_add(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def appointment_delete(request, id):
    user = request.user
    appointment = get_object_or_404(Appointment, id=id)
    if appointment.doctor != user:
        return Response({"detail": "You do not have permission to delete this review."}, status=status.HTTP_403_FORBIDDEN)
    if appointment.is_accepted:
        return Response({"detail": "Accepted Appointment can not deleted."}, status=status.HTTP_403_FORBIDDEN)
    appointment.delete()
    return Response({"detail": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def appointment_book(request, id):
    patient = request.user
    appointment = get_object_or_404(Appointment, id=id)
    if patient.is_doctor:
        return Response({"detail": "You must be a patient to book appointments."}, status=status.HTTP_403_FORBIDDEN)
    if not appointment.is_booked:
        appointment.is_booked = True
        appointment.patient = patient
        appointment.save()
        return Response({"detail": "Appointment booked successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "This appointment is already booked."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def booked_appointments(request, id):
    patient = get_object_or_404(User, id=id)
    appointments = Appointment.objects.filter(
        patient=patient, is_booked=True).order_by('appointment_date', 'start_time')
    grouped_appointments = {}

    for appointment in appointments:
        appointment_date = appointment.appointment_date
        if appointment_date not in grouped_appointments:
            grouped_appointments[appointment_date] = []
        grouped_appointments[appointment_date].append(appointment)

    data = []

    for appointment_date, appointments in grouped_appointments.items():
        doctor_data = UserSerializer(appointments[0].doctor).data
        patient_data = UserSerializer(
            appointments[0].patient).data if appointments[0].patient else None
        appointment_data = AppointmentSerializer(appointments, many=True).data

        data.append({
            'appointment_date': appointment_date,
            'doctor': doctor_data,
            'patient': patient_data,
            'appointments': appointment_data
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def booked_appointments_doctor(request, id):
    doctor = get_object_or_404(User, id=id)
    appointments = Appointment.objects.filter(
        doctor=doctor, is_booked=True).order_by('appointment_date', 'start_time')
    grouped_appointments = {}

    for appointment in appointments:
        appointment_date = appointment.appointment_date
        if appointment_date not in grouped_appointments:
            grouped_appointments[appointment_date] = []
        grouped_appointments[appointment_date].append(appointment)

    data = []

    for appointment_date, appointments in grouped_appointments.items():
        doctor_data = UserSerializer(appointments[0].doctor).data
        patient_data = UserSerializer(
            appointments[0].patient).data if appointments[0].patient else None
        appointment_data = AppointmentSerializer(appointments, many=True).data

        data.append({
            'appointment_date': appointment_date,
            'doctor': doctor_data,
            'patient': patient_data,
            'appointments': appointment_data
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def appointment_book_reject(request, id):
    doctor = request.user
    appointment = get_object_or_404(Appointment, id=id)
    if not doctor.is_doctor:
        return Response({"detail": "You must be a doctor to reject appointments."}, status=status.HTTP_403_FORBIDDEN)
    if appointment.is_booked and not appointment.is_accepted:
        appointment.is_booked = False
        appointment.patient = None
        appointment.save()
        return Response({"detail": "Appointment rejected successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "This appointment is already accepted."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def appointment_book_accept(request, id):
    doctor = request.user
    appointment = get_object_or_404(Appointment, id=id)
    if not doctor.is_doctor:
        return Response({"detail": "You must be a doctor to accept appointments."}, status=status.HTTP_403_FORBIDDEN)
    if appointment.is_booked and not appointment.is_accepted:
        appointment.is_accepted = True
        appointment.save()
        return Response({"detail": "Appointment accepted successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "This appointment is already accepted."}, status=status.HTTP_403_FORBIDDEN)
