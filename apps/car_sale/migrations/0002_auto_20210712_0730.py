# Generated by Django 3.2.5 on 2021-07-12 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_sale", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carsale",
            name="price",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="carsale",
            name="recycle",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="carsale",
            name="status",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="carsale",
            name="total",
            field=models.IntegerField(default=0),
        ),
    ]