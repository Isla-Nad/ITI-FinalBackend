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
        status = "Booked" if self.is_booked else "Available"
        patient_name = self.patient.get_full_name() if self.patient else "Not booked yet"
        acceptance_status = "Accepted" if self.is_accepted else "Pending"

        return f"Appointment with Dr. {self.doctor.last_name} on {self.appointment_date} ({self.start_time} - {self.end_time}): {status}. Patient: {patient_name}. Status: {acceptance_status}"
