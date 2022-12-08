# Generated by Django 4.1.3 on 2022-12-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0005_alter_transaction_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="transaction_date",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="transaction_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CREATED", "Created"),
                    ("COMPLETED", "Completed"),
                    ("SCHEDULED", "Scheduled"),
                    ("REQUESTED", "Requested"),
                    ("CANCELLED", "Cancelled"),
                ],
                default="Created",
                max_length=55,
                null=True,
            ),
        ),
    ]
