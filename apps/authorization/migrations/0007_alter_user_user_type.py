# Generated by Django 3.2.5 on 2021-08-14 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0006_auto_20210811_0524"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("superuser", "superuser"),
                    ("admin", "admin"),
                    ("sales_manager", "sales_manager"),
                    ("yard_manager", "yard_manager"),
                    ("client", "client"),
                    ("employee", "employee"),
                ],
                default="superuser",
                max_length=255,
            ),
        ),
    ]
