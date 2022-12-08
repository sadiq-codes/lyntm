from django.db import models
from django.contrib.auth import get_user_model
from djmoney.money import Money
from djmoney.models.fields import MoneyField
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password

from transactions.models import Transaction
from transactions.utils import generate_service_id


# Create your models here.


def make_transfer(amount, sender, receiver):
    type_list = [str, int, bool]
    if type(amount) in type_list:
        amount = Money(Decimal(amount), "USD")

    if amount > sender.balance:
        raise ValidationError("Insufficient funds")

    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wallet')
    account_number = models.CharField(max_length=11, db_index=True)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    pin = models.CharField(max_length=200, editable=False)
    created_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        return super(Wallet, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s wallet"

    @staticmethod
    def get_last_account_number():
        # Get the last account number
        wallet = Wallet.objects.last()
        return wallet.account_number

    @staticmethod
    def account_number_exists(account_number):
        return Wallet.objects.filter(account_number=account_number).__bool__()

    def generate_account_number(self):
        # Get the last used account number from the database
        last_account_number = self.get_last_account_number() or 0

        # Increment the last used account number by 1
        new_account_number = int(last_account_number) + 1

        while self.account_number_exists(new_account_number):
            # If the generated account number already exists, increment it by 1
            new_account_number += 1

        # Pad the account number with zeros to make it 11 digits long
        padded_account_number = f"{new_account_number:011d}"

        return padded_account_number

    def set_pin(self, pin):
        self.pin = make_password(password=pin)
        self.save()

    def check_pin(self, pin):
        return check_password(password=pin, encoded=self.pin)

    @classmethod
    def transfer(cls, sender, receiver, amount, category, notes, schedule=None):
        """
        :param sender:
        :param notes:
        :param category:
        :param amount:
        :param receiver:
        :param schedule:
        :type pin: object
        """
        make_transfer(amount, sender, receiver)
        Transaction.objects.create(amount=amount,
                                   sender=sender,
                                   receiver=receiver,
                                   transaction_category=category,
                                   notes=notes,
                                   transaction_status="COMPLETED")

    @classmethod
    def request_payment(cls, sender, receiver, amount, category, notes):
        Transaction.objects.create(amount=amount,
                                   sender=sender,
                                   receiver=receiver,
                                   transaction_category=category,
                                   notes=notes,
                                   transaction_status="REQUESTED")

    @staticmethod
    def accept_request(pk: object) -> object:
        transaction = Transaction.objects.get(pk=pk)
        make_transfer(transaction.amount, transaction.sender, transaction.receiver)
        transaction.transaction_status = "COMPLETED"
        transaction.save()

    @classmethod
    def schedule_payment(cls, sender, receiver, amount, category, notes):
        pass


class Service(models.Model):
    SERVICES_TYPE = (
        ("BILL", "Bill"),
        ("INSURANCE", "Insurance"),
        ("OPTION", "Option")
    )
    SERVICES_STATUS = (
        ('PAID', "Paid"),
        ("UNPAID", "Unpaid"),
        ("Failed", "failed")
    )
    name = models.CharField(max_length=250)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='service')
    customer_id = models.CharField(max_length=11, blank=True, null=True)
    service_type = models.CharField(choices=SERVICES_TYPE, max_length=55, blank=True, null=True)
    service_status = models.CharField(choices=SERVICES_STATUS, max_length=55, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            self.customer_id = generate_service_id()
        return super(Service, self).save(*args, **kwargs)

