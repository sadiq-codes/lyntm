from datetime import datetime
from celery import shared_task

# from django_celery_beat.models import PeriodicTask
# from celery.schedules import crontab
from transactions.models import Transaction


@shared_task
def schedule_payment_task(transaction_id, date_string):
    transaction = Transaction.objects.get(id=transaction_id)
    # Calculate the delay in seconds until the specified transfer time
    from .models import make_transfer
    now = datetime.now()
    date = datetime.fromisoformat(date_string)
    delay = (date - now).total_seconds()
    make_transfer(transaction.sender, transaction.receiver, transaction.amount)
    # Schedule the transfer to be carried out at the specified time
    schedule_payment_task.apply_async(args=transaction_id, countdown=delay)

# @app.task
# def transfer_money(transaction, date):
#     date_format = '%Y-%m-%d %H:%M:%S'
#     date = datetime.strptime(date, date_format)
#     # Schedule the transfer to be carried out at the specified time using the django-celery-beat package
#
#     periodic_task = PeriodicTask(
#         name='Transfer money from user {} to user {}'.format(transaction.sender, transaction.receiver),
#         task='tasks.transfer_money',
#         args=[transaction.sender, transaction.receiver, transaction.amount],
#         enabled=True,
#         crontab=crontab(hour=time.hour, minute=time.minute, second=time.second)
#     )
#     periodic_task.save()
#
#     # Carry out the transfer by updating the balance of each user
#     source_user.balance -= amount
#     destination_user.balance += amount
#     source_user.save()
#     destination_user.save()
