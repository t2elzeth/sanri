# Generated by Django 3.2.9 on 2021-11-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_alter_buyrequest_car"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buyrequest",
            name="approved",
        ),
        migrations.AddField(
            model_name="buyrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "pending"),
                    ("approved", "approved"),
                    ("declined", "declined"),
                ],
                default="pending",
                max_length=25,
            ),
        ),
    ]