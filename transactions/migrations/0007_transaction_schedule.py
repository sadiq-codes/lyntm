# Generated by Django 4.1.3 on 2022-12-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0006_alter_transaction_transaction_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="schedule",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]