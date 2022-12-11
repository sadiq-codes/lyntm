from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime, timedelta
from django.db.models import Sum, Q

from transactions.models import Transaction
from transactions.utils import generate_service_id

from .tasks import schedule_payment_task
from .utils import check_amount, make_transfer


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
        return wallet.account_number if wallet is not None else 0

    @staticmethod
    def account_number_exists(account_number):
        return Wallet.objects.filter(account_number=account_number).__bool__()

    def generate_account_number(self):
        # Get the last used account number from the database
        last_account_number = self.get_last_account_number()

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

    @property
    def get_sender_transactions(self):
        # Query the database to get all transactions where the wallet is the sender
        return Transaction.objects.filter(sender_wallet=self)

    @property
    def get_receiver_transactions(self):
        # Query the database to get all transactions where the wallet is the sender
        return Transaction.objects.filter(receiver_wallet=self)

    @property
    def get_all_user_transactions(self):
        # Query the database to get all transactions where the wallet is the sender and receiver
        transactions = self.get_sender_transactions | self.get_receiver_transactions
        return transactions

    @classmethod
    def deposit(cls, wallet, amount, category, notes):
        amount = check_amount(amount)

        wallet.balance += amount
        wallet.save()
        Transaction.objects.create(amount=amount,
                                   receiver=wallet,
                                   transaction_category=category,
                                   transaction_type="CREDIT",
                                   notes=notes,
                                   transaction_status="COMPLETED")

    @classmethod
    def withdraw(cls, wallet, amount, category, notes):
        amount = check_amount(amount)

        if amount > wallet.balance:
            raise ValidationError("Insufficient account balance,"
                                  " please try amount less than your balance")

        wallet.balance -= amount
        wallet.save()
        Transaction.objects.create(amount=amount,
                                   sender=wallet,
                                   transaction_category=category,
                                   transaction_type="DEBIT",
                                   notes=notes,
                                   transaction_status="COMPLETED")

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
        if schedule:
            Wallet.schedule_payment(sender, receiver, amount, category, notes, schedule)
        else:
            make_transfer(amount, sender, receiver)
            Transaction.objects.create(amount=amount,
                                       sender=sender,
                                       receiver=receiver,
                                       transaction_category=category,
                                       transaction_type="DEBIT",
                                       notes=notes,
                                       transaction_status="COMPLETED")

    @classmethod
    def request_payment(cls, sender, receiver, amount, category, notes):
        Transaction.objects.create(amount=amount,
                                   sender=sender,
                                   receiver=receiver,
                                   transaction_category=category,
                                   transaction_type="CREDIT",
                                   notes=notes,
                                   transaction_status="REQUESTED")

    @staticmethod
    def accept_request(pk: object) -> object:
        transaction = Transaction.objects.get(pk=pk)
        make_transfer(transaction.amount, transaction.sender, transaction.receiver)
        transaction.transaction_status = "COMPLETED"
        transaction.save()

    @classmethod
    def schedule_payment(cls, sender, receiver, amount, category, notes, schedule):
        print("i enter model schedule")
        transaction = Transaction.objects.create(amount=amount,
                                                 sender=sender,
                                                 receiver=receiver,
                                                 transaction_category=category,
                                                 notes=notes,
                                                 schedule=schedule,
                                                 transaction_status="SCHEDULED")
        print(transaction.id)
        schedule_payment_task(transaction.id, date_string=schedule)

    def get_statistics(self, time_period):
        # Retrieve the relevant income and expense data from the database using the Wallet object and time period
        if time_period == 'today':
            start_date = datetime.now() - timedelta(days=1)
            end_date = datetime.now()
        elif time_period == 'week':
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
        elif time_period == 'month':
            start_date = datetime.now() - timedelta(days=30)
            end_date = datetime.now()
        elif time_period == 'year':
            start_date = datetime.now() - timedelta(days=365)
            end_date = datetime.now()
        else:
            start_date = datetime.min
            end_date = datetime.max
        transactions = self.get_all_user_transactions.all()

        transactions = transactions.filter(transaction_date__range=(start_date, end_date)).order_by(
            'transaction_date')

        # transactions = transactions.filter(transaction_type=Transaction.)

        transactions_by_day = transactions.values('transaction_date').annotate(
            total_income=Sum('amount', filter=Q(transaction_type='CREDIT')),
            total_expense=Sum('amount',
                              filter=Q(transaction_type='DEBIT')))

        return transactions_by_day


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
