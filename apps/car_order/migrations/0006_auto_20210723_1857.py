# Generated by Django 3.2.5 on 2021-07-23 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_order', '0005_analysis'),
    ]

    operations = [
        migrations.AddField(
            model_name='carorder',
            name='analysis',
            field=models.JSONField(default=dict),
        ),
        migrations.DeleteModel(
            name='Analysis',
        ),
    ]
