from clinics.models import Clinic,Cases
from rest_framework import serializers



class ClinicSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=100)
    # desc = serializers.CharField()
    # image = serializers.ImageField(required=False)
    # address = serializers.CharField(max_length=100)
    # location = serializers.SerializerMethodField()
    
    # created_at = serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Clinic
        fields = "__all__"
    
class CaseSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Cases
        fields = "__all__"