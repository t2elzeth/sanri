# Generated by Django 3.2.5 on 2021-08-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0007_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='atWhatPrice',
            field=models.CharField(choices=[('by_fact', 'by_fact'), ('by_fob', 'by_fob'), ('by_fob2', 'by_fob2')], default='by_fact', max_length=255),
        ),
    ]