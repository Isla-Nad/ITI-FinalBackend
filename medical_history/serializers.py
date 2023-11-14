from rest_framework import serializers
from medical_history.models import MedicalHistory


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'
