# Generated by Django 3.2.9 on 2022-01-09 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0002_auto_20210906_0815"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffexpense",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]