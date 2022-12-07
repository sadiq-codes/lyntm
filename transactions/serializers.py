from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(max_length=4)

    class Meta:
        model = Transaction
        fields = ["sender", "receiver", "amount", "pin", "transaction_category"]
