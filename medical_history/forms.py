from medical_history.models import MedicalHistory
from django import forms
class Medical(forms.ModelForm):
    
    class Meta:
        model = MedicalHistory
        fields = "__all__"
class MedicalUpdate(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['patient_name', 'date_of_visit', 'allergies','medical_conditions','previous_dental_treatments','dental_conditions','dental_hygiene_habits','specific_dental_concerns','image']