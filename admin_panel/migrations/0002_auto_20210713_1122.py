# Generated by Django 3.2.5 on 2021-07-13 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='country_id',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='state_id',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='country_id',
            new_name='country',
        ),
    ]
