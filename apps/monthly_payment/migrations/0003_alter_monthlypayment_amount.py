# Generated by Django 3.2.9 on 2022-01-09 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monthly_payment", "0002_alter_monthlypayment_from_container"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlypayment",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
