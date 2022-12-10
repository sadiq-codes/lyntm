from rest_framework import serializers

from wallets.serializers import WalletSerializer
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["id", "reference", "sender_wallet", "receiver_wallet", "amount", "transaction_date",
                  "transaction_category", "transaction_status", "transaction_type", "notes", "schedule"]

    def get_transaction_type(self, obj):
        request = self.context.get("request")
        wallet = request.user.wallet
        return obj.get_transaction_type_for_wallet(wallet)

