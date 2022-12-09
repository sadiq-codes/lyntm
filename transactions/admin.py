from django.contrib import admin
from .models import Transaction
# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["sender_wallet", "receiver_wallet", "transaction_type", "amount", "reference", "transaction_status", ]
