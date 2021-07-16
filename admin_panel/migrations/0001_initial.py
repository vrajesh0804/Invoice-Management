# Generated by Django 3.2.5 on 2021-07-13 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'countries',
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
                ('country_id', models.CharField(default='', max_length=255)),
                ('state_id', models.CharField(default='', max_length=255)),
                ('city_id', models.CharField(default='', max_length=255)),
                ('logo', models.ImageField(default='', upload_to='uploads/')),
                ('no_of_offices', models.IntegerField(default=0)),
                ('no_of_employees', models.IntegerField(default=0)),
                ('established_in', models.IntegerField(default=0)),
                ('total_amount_spend', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'customer',
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
                ('name', models.CharField(max_length=255, null=True)),
                ('country_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.country')),
            ],
            options={
                'db_table': 'states',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('country_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.country')),
                ('state_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.state')),
            ],
            options={
                'db_table': 'cities',
            },
        ),
    ]