# Generated by Django 3.2.7 on 2021-09-19 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_rename_position_userarea_up'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userarea',
            name='user',
            field=models.CharField(max_length=145, null=True),
        ),
    ]