# Generated by Django 3.2.5 on 2021-09-01 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("container", "0001_initial"),
        ("monthly_payment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlypayment",
            name="from_container",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="monthly_payments",
                to="container.container",
            ),
        ),
    ]
