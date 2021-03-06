# Generated by Django 3.2.5 on 2021-09-06 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staffexpense",
            name="staff_members",
        ),
        migrations.AddField(
            model_name="staffexpense",
            name="staff_member",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expenses",
                to="staff.staffmember",
            ),
            preserve_default=False,
        ),
    ]
