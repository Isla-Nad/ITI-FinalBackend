from django.db import models
# from django.contrib.gis.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)    
    image = models.ImageField(upload_to= 'clinics/images/')
    address = models.CharField(max_length=100)
    # location = models.PointField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    
    
    
    def __str__(self):
        return f'{self.name}'
    
    @classmethod
    def get_all_clinics(cls):
        return cls.objects.all()
    
    


class Cases(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(
        upload_to='clinics/images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
    
    # def get_cases_for_clinic(self, clinic_id):
    #     cases_for_clinic = Cases.objects.filter(clinic_id=clinic_id)
    #     return cases_for_clinic
    
