# Generated by Django 3.2.5 on 2021-07-18 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CarStore",
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
                    "brand",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "model",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "year",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "milage",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "body",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "displacement",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "complect",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "condition",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "price",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "status",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CarStoreImage",
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
                ("name", models.ImageField(upload_to="")),
                (
                    "car_store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="car_store.carstore",
                    ),
                ),
            ],
        ),
    ]
