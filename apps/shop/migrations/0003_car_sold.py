# Generated by Django 3.2.9 on 2021-11-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_buyrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="sold",
            field=models.BooleanField(default=False),
        ),
    ]
