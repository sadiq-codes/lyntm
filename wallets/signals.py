from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from djmoney.money import Money

from .models import Wallet


@receiver(post_save, sender=get_user_model())
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance,
                              balance=Money(0.0, "USD"))
