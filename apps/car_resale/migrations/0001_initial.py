# Generated by Django 3.2.5 on 2021-08-26 19:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authorization", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("car_order", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarResale",
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
                ("startingPrice", models.IntegerField()),
                ("salePrice", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "carOrder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="car_resales",
                        to="car_order.carorder",
                    ),
                ),
                (
                    "newClient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="car_resales_as_new_client",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "oldClient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="car_resales_as_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="CarResaleOldClientReplenishment",
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
                (
                    "balance",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="old_client_replenishment",
                        to="authorization.balance",
                    ),
                ),
                (
                    "car_resale",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="old_client_replenishment",
                        to="car_resale.carresale",
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="CarResaleNewClientWithdrawal",
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
                (
                    "balance",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="new_client_withdrawal",
                        to="authorization.balance",
                    ),
                ),
                (
                    "car_resale",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="new_client_withdrawal",
                        to="car_resale.carresale",
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
    ]
