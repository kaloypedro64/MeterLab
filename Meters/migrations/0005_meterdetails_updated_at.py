# Generated by Django 3.2.7 on 2022-01-21 02:03

from django.db import migrations, models
import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        ('Meters', '0004_auto_20220120_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='meterdetails',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=sqlalchemy.sql.expression.true),
            preserve_default=sqlalchemy.sql.expression.true,
        ),
    ]
