# Generated by Django 3.2.9 on 2021-11-09 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_carimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrequest',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_requests', to='shop.car'),
        ),
    ]
