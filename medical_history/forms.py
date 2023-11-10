from medical_history.models import MedicalHistory
from django import forms
class Medical(forms.ModelForm):
    
    class Meta:
        model = MedicalHistory
        fields = "__all__"
