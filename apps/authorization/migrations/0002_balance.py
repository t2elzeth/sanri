# Generated by Django 3.2.4 on 2021-06-30 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Balance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("sum_in_jpy", models.IntegerField()),
                ("sum_in_usa", models.IntegerField()),
                ("rate", models.IntegerField()),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("cashless", "cashless"), ("cash", "cash")],
                        max_length=255,
                    ),
                ),
                ("sender_name", models.CharField(max_length=255)),
                ("comment", models.TextField()),
                (
                    "balance_action",
                    models.CharField(
                        choices=[
                            ("replenishment", "replenishment"),
                            ("withdrawal", "withdrawal"),
                        ],
                        max_length=255,
                    ),
                ),
            ],
        ),
    ]