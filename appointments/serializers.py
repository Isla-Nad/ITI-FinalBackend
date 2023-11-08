from rest_framework import serializers
from appointments.models import Appointment
from django.core.exceptions import ValidationError
from django.utils import timezone


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        appointment_date = data.get('appointment_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if appointment_date and appointment_date < timezone.now().date():
            raise ValidationError("Appointment date cannot be in the past.")

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be greater than start time.")

        return data
