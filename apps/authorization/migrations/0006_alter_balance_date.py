# Generated by Django 3.2.5 on 2021-07-11 21:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0005_alter_user_sizefob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balance",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]