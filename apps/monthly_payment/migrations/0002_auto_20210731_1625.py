# Generated by Django 3.2.5 on 2021-07-31 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monthlypayment',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='monthlypaymenttype',
            options={'ordering': ('id',)},
        ),
    ]
