from decimal import Decimal
from djmoney.money import Money
from django.core.exceptions import ValidationError


def check_amount(amount):
    type_list = [str, int, bool]
    # Check if type of amount is in list and convert it to money object
    if type(amount) in type_list:
        amount = Money(Decimal(amount), "USD")
    return amount


def make_transfer(amount, sender, receiver):
    amount = check_amount(amount)
    if amount > sender.balance:
        raise ValidationError("Insufficient funds")

    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()

