# Generated by Django 3.2.5 on 2021-07-21 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_auto_20210721_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='city',
            new_name='city_id',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='country',
            new_name='country_id',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='state',
            new_name='state_id',
        ),
    ]