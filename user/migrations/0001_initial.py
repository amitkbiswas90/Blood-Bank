# Generated by Django 4.2.11 on 2025-04-08 12:15

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(100)])),
                ('blood_group', models.CharField(choices=[('A+', 'A Positive'), ('A-', 'A Negative'), ('B+', 'B Positive'), ('B-', 'B Negative'), ('AB+', 'AB Positive'), ('AB-', 'AB Negative'), ('O+', 'O Positive'), ('O-', 'O Negative')], max_length=3)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')])),
                ('address', models.TextField(blank=True, null=True)),
                ('last_donation_date', models.DateField(blank=True, max_length=300, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
