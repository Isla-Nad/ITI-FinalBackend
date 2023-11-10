from django.db import models
from accounts.models import User

# Create your models here.


class Appointment(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='patient_appointments', null=True, blank=True)
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['appointment_date', 'start_time', 'end_time']

    def __str__(self):
        return f"Appointment with {self.doctor.first_name} on {self.appointment_date}"
