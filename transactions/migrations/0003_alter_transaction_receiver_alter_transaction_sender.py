# Generated by Django 4.1.3 on 2022-12-07 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0003_service"),
        ("transactions", "0002_rename_ref_transaction_reference"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receiver",
                to="wallets.wallet",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender",
                to="wallets.wallet",
            ),
        ),
    ]