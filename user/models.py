from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from user.CustomUserManager import CustomUserManager


class User(AbstractUser):

    BLOOD_GROUP_CHOICES = [
        ('A_plus', 'A+'),
        ('A_minus', 'A-'),
        ('B_plus', 'B+'),
        ('B_minus', 'B-'),
        ('AB_plus', 'AB+'),
        ('AB_minus', 'AB-'),
        ('O_plus', 'O+'),
        ('O_minus', 'O-'),
    ]

    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    blood_group = models.CharField(
        max_length=8, 
        choices=BLOOD_GROUP_CHOICES
    )
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        null=True,
        blank=True
    )
    address = models.TextField(null=True, blank=True)
    last_donation_date = models.DateField(max_length=300,null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email