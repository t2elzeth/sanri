# Generated by Django 3.2.5 on 2021-07-11 21:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("income", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="income",
            name="comment",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="income",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
