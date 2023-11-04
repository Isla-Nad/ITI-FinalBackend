from rest_framework import serializers
from medicalHistory.models import MedicalHistory
class MedicalSerlizer(serializers.Serializer):
    id = serializers.IntegerField()
    patient_name=serializers.CharField(max_length=200)
    date_of_visit=serializers.DateField()
    action=serializers.CharField()
