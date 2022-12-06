from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class CustomUser(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    SELECT = 'S'

    gender_choice = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (SELECT, 'Select')

    ]

    country = CountryField(blank_label='(select country)')
    phone_number = PhoneNumberField(blank=True)
    pin = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    gender = models.CharField(choices=gender_choice, default=SELECT, max_length=2)
    address = models.CharField(max_length=200, blank=True)
