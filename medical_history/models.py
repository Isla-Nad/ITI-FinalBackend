from django.db import models
from accounts.models import User


class MedicalHistory(models.Model):
    doctor = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    date_of_visit = models.DateField()
    allergies = models.CharField(
        default="", null=True, blank=True)
    medical_conditions = models.CharField(
        default="", null=True, blank=True)
    previous_dental_treatments = models.CharField(
        default="", null=True, blank=True)
    dental_conditions = models.CharField(
        default="", null=True, blank=True)
    dental_hygiene_habits = models.CharField(
        default="", null=True, blank=True)
    specific_dental_concerns = models.CharField(
        default="", null=True, blank=True)
    image = models.ImageField(
        upload_to='medical_history/images/', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name}"
    def get_image_url(self):
        return f'/media/{self.image}'
