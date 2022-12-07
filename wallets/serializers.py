from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Wallet


class PinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4)


class WalletSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Wallet
        fields = ("id", "account_number", "balance", "balance_currency", "user")
