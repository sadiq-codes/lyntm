# Generated by Django 4.1.3 on 2022-12-07 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_customuser_address_customuser_date_of_birth_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="pin",
        ),
    ]