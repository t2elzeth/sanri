# Generated by Django 3.2.4 on 2021-06-20 06:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                (
                    "startingPrice",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "salePrice",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "income",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
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
                    "ownerClient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="car_resales_as_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
