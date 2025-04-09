from rest_framework import serializers
from blood.models import BloodRequest
from user.models import User
from django.utils import timezone
from datetime import timedelta


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = [
            'id', 
            'requester', 
            'blood_group',
            'units_required', 
            'status', 
            'hospital_name', 
            'hospital_address', 
            'needed_by', 
            'created_at'
        ]
        read_only_fields = ['created_at', 'requester', 'status']


class DonorSerializer(serializers.ModelSerializer):
    eligibility_status = serializers.SerializerMethodField()
    last_donation = serializers.DateField(source='last_donation_date')

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'blood_group',
            'age',
            'last_donation',
            'eligibility_status'
        ]
        read_only_fields = fields

    def get_eligibility_status(self, obj):
        if not obj.last_donation_date:
            return "Eligible"
            
        three_months_ago = timezone.now().date() - timedelta(days=90)
        return "Eligible" if obj.last_donation_date < three_months_ago else "Not Eligible"
    

class DonationHistorySerializer(serializers.ModelSerializer):
    requester_name = serializers.ReadOnlyField(source='requester.get_full_name')
    hospital_info = serializers.SerializerMethodField()
    
    class Meta:
        model = BloodRequest
        fields = [
            'id', 
            'blood_group', 
            'units_required', 
            'status', 
            'created_at', 
            'requester_name', 
            'hospital_info'
        ]
    
    def get_hospital_info(self, obj):
        return f"{obj.hospital_name}, {obj.hospital_address}"