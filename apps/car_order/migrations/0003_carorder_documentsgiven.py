# Generated by Django 3.2.5 on 2021-07-11 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_order", "0002_alter_carorder_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="carorder",
            name="documentsGiven",
            field=models.BooleanField(default=False),
        ),
    ]
