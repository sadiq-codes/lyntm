from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField

from users.serializers import CustomUserSerializer
from .models import Wallet


class PinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4)


class WalletSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Wallet
        fields = ("id", "account_number", "balance", "balance_currency", "user")


class DepositSerializer(serializers.Serializer):
    amount = MoneyField(max_digits=10, decimal_places=2)
    transaction_category = serializers.CharField(max_length=250, allow_blank=True)
    notes = serializers.CharField(max_length=250)
