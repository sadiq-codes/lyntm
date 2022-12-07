from django.db import models
from django.contrib.auth import get_user_model
from djmoney.money import Money
from djmoney.models.fields import MoneyField
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password

from transactions.models import Transaction


# Create your models here.


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
    def transfer(cls, sender, receiver, amount, category, notes, pin, schedule=None):
        """

        :param sender:
        :param notes:
        :param category:
        :param amount:
        :param receiver:
        :param schedule:
        :type pin: object
        """
        amount = Money(Decimal(amount), "USD")
        if not sender.check_pin(pin):
            print(pin)
            raise ValidationError("incorrect wallet pin")

        if amount > sender.balance:
            raise ValidationError("Insufficient funds")

        if schedule:
            pass

        sender.balance - amount
        # receiver.balance += amount

        Transaction.objects.create(amount=amount,
                                   sender=sender,
                                   receiver=receiver,
                                   transaction_category=category,
                                   notes=notes,
                                   transaction_status="Completed")

        sender.save()
        receiver.save()


class Service(models.Model):
    pass
