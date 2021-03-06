# Generated by Django 3.2.5 on 2021-08-26 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Auction",
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
                    "name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "parkingPrice1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "parkingPrice2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "parkingPrice3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "parkingPrice4",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
    ]
