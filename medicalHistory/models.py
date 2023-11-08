from django.db import models

# Create your models here.
class MedicalHistory(models.Model):
    patient_name= models.CharField(max_length=100)
    date_of_visit= models.DateField()
    Allergies=models.TextField(default="enter")
    MedicalConditions=models.TextField(default="enter")
    PreviouDentalTreatments=models.TextField(default="enter")
    DentalConditions=models.TextField(default="enter")
    DentalHygieneHabits=models.TextField(default="enter")
    image=models.ImageField(upload_to='medicalhistory/images/',max_length=200 ,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"
    def get_image_url(self):
        return f'/media/{self.image}'