# Generated by Django 4.2.11 on 2025-04-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A Positive'), ('A-', 'A Negative'), ('B+', 'B Positive'), ('B-', 'B Negative'), ('AB+', 'AB Positive'), ('AB-', 'AB Negative'), ('O+', 'O Positive'), ('O-', 'O Negative')], max_length=3)),
                ('units_required', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10)),
                ('hospital_name', models.CharField(max_length=200)),
                ('hospital_address', models.TextField(blank=True, null=True)),
                ('needed_by', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
