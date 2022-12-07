from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password


# Create your models here.


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wallet')
    account_number = models.CharField(max_length=11)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    pin = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now=True)
