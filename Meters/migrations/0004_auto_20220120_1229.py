# Generated by Django 3.2.7 on 2022-01-20 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Meters', '0003_alter_meterseal_meterdetailsid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metertest',
            name='kh',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='metertest',
            name='phase',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='metertest',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='metertest',
            name='ta',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='metertest',
            name='type',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='metertest',
            name='volts',
            field=models.CharField(max_length=15),
        ),
    ]