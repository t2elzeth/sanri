# Generated by Django 3.2.5 on 2021-08-26 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_order', '0001_initial'),
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('dateOfSending', models.DateField()),
                ('commission', models.IntegerField()),
                ('containerTransportation', models.IntegerField()),
                ('packagingMaterials', models.IntegerField()),
                ('transportation', models.IntegerField()),
                ('loading', models.IntegerField()),
                ('status', models.CharField(choices=[('going_to', 'going_to'), ('shipped', 'shipped')], max_length=255)),
                ('totalAmount', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='containers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='WheelSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('sum', models.IntegerField()),
                ('container', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wheel_sales', to='container.container')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='WheelRecycling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('sum', models.IntegerField()),
                ('container', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wheel_recycling', to='container.container')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ContainerCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='container_cars', to='car_order.carorder')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='container_cars', to='container.container')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ContainerBalanceWithdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='container_withdrawal', to='authorization.balance')),
                ('container', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='container_withdrawal', to='container.container')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
