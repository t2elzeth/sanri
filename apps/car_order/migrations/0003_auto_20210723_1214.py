# Generated by Django 3.2.5 on 2021-07-23 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_auto_20210723_1214'),
        ('car_order', '0002_balancereplenishment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceWithdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car_order_withdrawals', to='authorization.balance')),
                ('car_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='replenishment', to='car_order.carorder')),
            ],
        ),
        migrations.DeleteModel(
            name='BalanceReplenishment',
        ),
    ]
