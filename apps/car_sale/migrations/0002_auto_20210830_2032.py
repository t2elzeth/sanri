# Generated by Django 3.2.5 on 2021-08-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_sale", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="carsale",
            name="carModel",
            field=models.CharField(default=1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="carsale",
            name="vinNumber",
            field=models.CharField(default=1, max_length=512),
            preserve_default=False,
        ),
    ]