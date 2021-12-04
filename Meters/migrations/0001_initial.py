# Generated by Django 3.2.7 on 2021-12-02 09:33

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='acquisition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transactiondate', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('rrnumber', models.CharField(db_index=True, max_length=145)),
                ('area', models.PositiveSmallIntegerField(default=0)),
                ('userid', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acqtype', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'acquisition',
            },
        ),
        migrations.CreateModel(
            name='brands',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(db_index=True, max_length=45)),
            ],
            options={
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='consumers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('consumer', models.CharField(max_length=145, null=True)),
                ('address', models.CharField(max_length=145, null=True)),
                ('type', models.CharField(max_length=2, null=True)),
                ('active', models.PositiveSmallIntegerField(default=0, null=True)),
            ],
            options={
                'db_table': 'consumers',
            },
        ),
        migrations.CreateModel(
            name='meterdetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('serialno', models.CharField(max_length=45)),
                ('accuracy', models.CharField(max_length=45, null=True)),
                ('wms_status', models.PositiveSmallIntegerField(default=0, null=True)),
                ('status', models.PositiveSmallIntegerField(default=0, null=True)),
                ('active', models.PositiveSmallIntegerField(default=0, null=True)),
            ],
            options={
                'db_table': 'meterdetails',
            },
        ),
        migrations.CreateModel(
            name='mtype',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('metertype', models.CharField(db_index=True, max_length=45)),
            ],
            options={
                'db_table': 'metertype',
            },
        ),
        migrations.CreateModel(
            name='suppliers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('suppliername', models.CharField(max_length=145)),
                ('address', models.CharField(max_length=145, null=True)),
            ],
            options={
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='seals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('boxes', models.IntegerField(default=0)),
                ('ppb', models.IntegerField(default=0)),
                ('serialnos', models.CharField(max_length=45, null=True)),
                ('acquisitionid', models.ForeignKey(db_column='acquisitionid', on_delete=django.db.models.deletion.PROTECT, to='Meters.acquisition')),
                ('brandid', models.ForeignKey(db_column='brandid', on_delete=django.db.models.deletion.PROTECT, to='Meters.brands')),
            ],
            options={
                'db_table': 'seals',
            },
        ),
        migrations.CreateModel(
            name='sealdetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('serialno', models.CharField(max_length=45)),
                ('techcrew', models.CharField(max_length=45, null=True)),
                ('status', models.PositiveSmallIntegerField(default=0, null=True)),
                ('active', models.PositiveSmallIntegerField(default=0, null=True)),
                ('meterdetailsid', models.ForeignKey(db_column='meterdetailsid', null=True, on_delete=django.db.models.deletion.PROTECT, to='Meters.meterdetails')),
                ('sealid', models.ForeignKey(db_column='sealid', on_delete=django.db.models.deletion.CASCADE, to='Meters.seals')),
            ],
            options={
                'db_table': 'sealdetails',
            },
        ),
        migrations.CreateModel(
            name='metertest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('testdate', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('serialno', models.CharField(max_length=15)),
                ('gen_average', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fullload_average', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('lightload_average', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fl1', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fl2', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('fl3', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('ll1', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('ll2', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('ll3', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('reading', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('type', models.PositiveSmallIntegerField(default=0, null=True)),
                ('volts', models.CharField(max_length=45)),
                ('phase', models.CharField(max_length=45)),
                ('kh', models.CharField(max_length=45)),
                ('ta', models.CharField(max_length=45)),
                ('remarks', models.CharField(max_length=245)),
                ('active', models.PositiveSmallIntegerField(default=0, null=True)),
                ('isdamage', models.BooleanField(default=False)),
                ('userid', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('consumersid', models.ForeignKey(db_column='consumers', on_delete=django.db.models.deletion.CASCADE, to='Meters.consumers')),
            ],
            options={
                'db_table': 'metertest',
            },
        ),
        migrations.CreateModel(
            name='meterseal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transactiondate', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('seal_a', models.CharField(max_length=45, null=True)),
                ('seal_b', models.CharField(max_length=45, null=True)),
                ('metercondition', models.PositiveSmallIntegerField(default=0, null=True)),
                ('accuracy', models.IntegerField(default=0)),
                ('reading', models.IntegerField(default=0)),
                ('remarks', models.CharField(max_length=245)),
                ('active', models.PositiveSmallIntegerField(default=0, null=True)),
                ('userid', models.CharField(max_length=45)),
                ('meterdetailsid', models.ForeignKey(db_column='meterdetailsid', on_delete=django.db.models.deletion.PROTECT, to='Meters.meterdetails')),
            ],
            options={
                'db_table': 'meterseal',
            },
        ),
        migrations.CreateModel(
            name='meters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ampheres', models.CharField(max_length=45, null=True)),
                ('serialnos', models.CharField(max_length=145, null=True)),
                ('units', models.IntegerField(default=0)),
                ('acquisitionid', models.ForeignKey(db_column='acquisitionid', on_delete=django.db.models.deletion.PROTECT, to='Meters.acquisition')),
                ('brandid', models.ForeignKey(db_column='brandid', on_delete=django.db.models.deletion.PROTECT, to='Meters.brands')),
                ('mtypeid', models.ForeignKey(db_column='mtypeid', on_delete=django.db.models.deletion.PROTECT, to='Meters.mtype')),
            ],
            options={
                'db_table': 'meters',
            },
        ),
        migrations.AddField(
            model_name='meterdetails',
            name='meterid',
            field=models.ForeignKey(db_column='meterid', on_delete=django.db.models.deletion.CASCADE, to='Meters.meters'),
        ),
        migrations.AddField(
            model_name='acquisition',
            name='supplierid',
            field=models.ForeignKey(db_column='supplierid', on_delete=django.db.models.deletion.PROTECT, related_name='suppliers', to='Meters.suppliers'),
        ),
    ]
