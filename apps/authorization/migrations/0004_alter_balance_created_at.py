# Generated by Django 3.2.9 on 2022-01-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorization", "0003_user_transportation_limit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balance",
            name="created_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]
