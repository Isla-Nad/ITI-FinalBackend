from django import forms
from clinics.models import Clinic

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = "__all__"
