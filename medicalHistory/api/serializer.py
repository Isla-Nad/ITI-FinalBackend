from rest_framework import serializers
from medicalHistory.models import MedicalHistory
class MedicalSerlizer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'    

