# Generated by Django 3.2.5 on 2021-07-22 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_invoice_symbol'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='symbol',
            new_name='currency_symbol',
        ),
    ]
