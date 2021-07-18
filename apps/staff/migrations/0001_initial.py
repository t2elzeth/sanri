# Generated by Django 3.2.5 on 2021-07-18 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaffExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('visa', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('visa_expiration_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.CharField(max_length=255)),
                ('comment', models.TextField()),
                ('staff_members', models.ManyToManyField(to='staff.StaffMember')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_expenses', to='staff.staffexpensetype')),
            ],
        ),
    ]
