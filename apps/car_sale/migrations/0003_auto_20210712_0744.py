# Generated by Django 3.2.5 on 2021-07-12 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_order', '0005_alter_carorder_amount'),
        ('car_sale', '0002_auto_20210712_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carsale',
            name='carModel',
        ),
        migrations.RemoveField(
            model_name='carsale',
            name='vinNumber',
        ),
        migrations.AddField(
            model_name='carsale',
            name='carOrder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='car_sales', to='car_order.carorder'),
            preserve_default=False,
        ),
    ]
