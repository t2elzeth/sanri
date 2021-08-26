# Generated by Django 3.2.5 on 2021-08-26 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('currency', models.CharField(choices=[('usd', 'usd'), ('jpy', 'jpy')], max_length=255)),
                ('hp', models.IntegerField()),
                ('engine', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('millage', models.IntegerField()),
                ('condition', models.FloatField()),
                ('body', models.CharField(max_length=255)),
                ('displacement', models.CharField(max_length=255)),
                ('complect', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('for_sell', 'for_sell'), ('for_approve', 'for_approve'), ('sold', 'sold')], default='for_sell', max_length=255)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_cars', to='car_model.carmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ShopImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.shopcar')),
            ],
        ),
        migrations.CreateModel(
            name='FuelEfficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.FloatField()),
                ('track', models.FloatField()),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fuel_efficiency', to='shop.shopcar')),
            ],
        ),
        migrations.CreateModel(
            name='CarForApprove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='for_approve', to=settings.AUTH_USER_MODEL)),
                ('shop_car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='for_approve', to='shop.shopcar')),
            ],
        ),
    ]
