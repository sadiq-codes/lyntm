from django.db import models
from djmoney.models.fields import MoneyField
from datetime import datetime, timedelta
from django.db.models import Sum, Q

# Create your models here.
import wallets.models
from .utils import generate_transaction_ref_code


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    )
    TRANSACTION_STATUS = (
        ("CREATED", "Created"),
        ("COMPLETED", "Completed"),
        ("SCHEDULED", "Scheduled"),
        ("REQUESTED", "Requested"),
        ("CANCELLED", "Cancelled")
    )
    TRANSACTION_CATEGORY = (
        ("FAMILY", "Family"),
        ("BUSINESS", "Business"),
        ("FOOD & DRINKS", "Food & Drinks"),
    )
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    reference = models.CharField(max_length=200, unique=True, blank=True)

    sender_wallet = models.ForeignKey("wallets.Wallet", on_delete=models.CASCADE, related_name='sender_transactions')
    receiver_wallet = models.ForeignKey("wallets.Wallet", on_delete=models.CASCADE,
                                        related_name='receiver_transactions')

    transaction_date = models.DateTimeField(auto_now=True, db_index=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=55, blank=True, null=True)
    transaction_status = models.CharField(choices=TRANSACTION_STATUS, max_length=55, blank=True, null=True,
                                          default="Created")
    transaction_category = models.CharField(choices=TRANSACTION_CATEGORY, max_length=55, blank=True, null=True)
    schedule = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_transaction_ref_code()
        return super(Transaction, self).save(*args, **kwargs)

    def get_transaction_type_for_wallet(self, wallet):
        if wallet == self.sender_wallet:
            return "Debit"
        elif wallet == self.receiver_wallet:
            return "Credit"
        else:
            return "N/A"