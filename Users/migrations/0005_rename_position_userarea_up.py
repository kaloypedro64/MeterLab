# Generated by Django 3.2.7 on 2021-09-19 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20210919_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userarea',
            old_name='position',
            new_name='up',
        ),
    ]
