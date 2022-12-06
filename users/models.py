from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class CustomUser(AbstractUser):
    country = CountryField(blank_label='(select country)')
    phone_number = PhoneNumberField(blank=True)
    pin = models.CharField(max_length=100)
