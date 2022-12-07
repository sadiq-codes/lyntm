from rest_framework import serializers

from wallets.serializers import WalletSerializer
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["id", "sender", "receiver", "amount", "transaction_category"]
