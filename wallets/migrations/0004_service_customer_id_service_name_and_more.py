# Generated by Django 4.1.3 on 2022-12-08 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0003_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="customer_id",
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="name",
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="service_status",
            field=models.CharField(
                blank=True,
                choices=[("PAID", "Paid"), ("UNPAID", "Unpaid"), ("Failed", "failed")],
                max_length=55,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="service_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("BILL", "Bill"),
                    ("INSURANCE", "Insurance"),
                    ("OPTION", "Option"),
                ],
                max_length=55,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="wallet",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="service",
                to="wallets.wallet",
            ),
            preserve_default=False,
        ),
    ]
