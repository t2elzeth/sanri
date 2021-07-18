# Generated by Django 3.2.5 on 2021-07-18 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('fullName', models.CharField(max_length=255)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=255, null=True)),
                ('service', models.CharField(choices=[('dissection', 'dissection'), ('entire', 'entire')], default='entire', max_length=255)),
                ('atWhatPrice', models.CharField(choices=[('by_fact', 'by_fact'), ('by_fob', 'by_fob')], default='by_fact', max_length=255)),
                ('sizeFOB', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=16, unique=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('user_type', models.CharField(choices=[('user', 'user'), ('client', 'client'), ('employee', 'employee')], default='user', max_length=255)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('sum_in_jpy', models.IntegerField()),
                ('sum_in_usa', models.IntegerField()),
                ('rate', models.IntegerField()),
                ('payment_type', models.CharField(choices=[('cashless', 'cashless'), ('cash', 'cash')], max_length=255)),
                ('sender_name', models.CharField(max_length=255)),
                ('comment', models.TextField()),
                ('balance_action', models.CharField(choices=[('replenishment', 'replenishment'), ('withdrawal', 'withdrawal')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
