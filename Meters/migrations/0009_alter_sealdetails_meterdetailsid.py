# Generated by Django 3.2.7 on 2021-10-13 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Meters', '0008_sealdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sealdetails',
            name='meterdetailsid',
            field=models.ForeignKey(db_column='meterdetailsid', null=True, on_delete=django.db.models.deletion.PROTECT, to='Meters.meterdetails'),
        ),
    ]
