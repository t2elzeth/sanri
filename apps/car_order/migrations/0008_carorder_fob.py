# Generated by Django 3.2.9 on 2021-11-16 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_order", "0007_carorder_is_shipped"),
    ]

    operations = [
        migrations.AddField(
            model_name="carorder",
            name="fob",
            field=models.IntegerField(default=0),
        ),
    ]
