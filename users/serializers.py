from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from phonenumber_field.serializerfields import PhoneNumberField
from .models import CustomUser


class CustomUserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    phone_number = PhoneNumberField(allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "country", "phone_number", \
                  "date_of_birth", "gender", "address",)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("image",)
