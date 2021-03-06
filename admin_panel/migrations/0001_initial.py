# Generated by Django 3.2.5 on 2021-07-21 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('purpose', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('customer_id', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'invoice',
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'login_data',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.country')),
            ],
            options={
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(default='', max_length=255)),
                ('company_name', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default='', max_length=255)),
                ('phone', models.IntegerField(default=0)),
                ('email', models.EmailField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('total_spending', models.IntegerField(blank='True', default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.state')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.state'),
        ),
    ]
