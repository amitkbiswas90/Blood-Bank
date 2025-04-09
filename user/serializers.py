from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'name', 'age', 'blood_group', 
                 'phone', 'address', 'last_donation_date', 
                 'is_available', 'is_active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'age', 'blood_group', 
                 'phone', 'address']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            **{k: v for k, v in validated_data.items() if k != 'email' and k != 'password'},
            is_active=True
        )
        return user