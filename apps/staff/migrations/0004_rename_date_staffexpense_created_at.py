# Generated by Django 3.2.9 on 2022-01-21 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0003_alter_staffexpense_amount"),
    ]

    operations = [
        migrations.RenameField(
            model_name="staffexpense",
            old_name="date",
            new_name="created_at",
        ),
    ]
