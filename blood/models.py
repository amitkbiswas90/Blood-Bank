from django.db import models
from user.models import User

# Create your models here.
class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests_created'
    )
    donor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests_accepted'
    )
    blood_group = models.CharField(
        max_length=8,  # Changed from 3 to 8
        choices=User.BLOOD_GROUP_CHOICES
    )
    units_required = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField(null=True, blank=True)
    needed_by = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester}'s {self.blood_group} request"