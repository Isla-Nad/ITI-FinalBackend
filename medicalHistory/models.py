from django.db import models

# Create your models here.
class MedicalHistory(models.Model):
    patient_name= models.CharField(max_length=100)
    date_of_visit= models.DateField()
    action= models.CharField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"