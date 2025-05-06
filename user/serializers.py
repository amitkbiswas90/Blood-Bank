from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    days_since_last_donation = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'name', 'age', 'blood_group', 
                 'phone', 'address', 'last_donation_date', 
                 'is_available', 'is_active', 'days_since_last_donation']
        extra_kwargs = {
            'last_donation_date': {
                'allow_null': True,
                'required': False
            }
        }

    def get_days_since_last_donation(self, obj):
        if obj.last_donation_date:
            return (timezone.now().date() - obj.last_donation_date).days
        return None

    def validate_last_donation_date(self, value):
        if value and value > timezone.now().date():
            # Get previous valid date for existing users
            if self.instance and self.instance.last_donation_date:
                raise serializers.ValidationError(
                    f"Future dates not allowed. Last valid donation: {self.instance.last_donation_date}"
            )
            raise serializers.ValidationError("Donation date cannot be in the future")
        return value

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'age', 'blood_group', 
                 'phone', 'address', 'last_donation_date']
        extra_kwargs = {
            'last_donation_date': {
                'allow_null': True,
                'required': False
            }
        }

    def validate_last_donation_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Donation date cannot be in the future")
        return value

    def create(self, validated_data):
        # Explicit field assignment for security
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name'),
            age=validated_data.get('age'),
            blood_group=validated_data.get('blood_group'),
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
            last_donation_date=validated_data.get('last_donation_date'),
            is_active=True
        )
        return user