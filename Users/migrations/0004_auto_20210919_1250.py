# Generated by Django 3.2.7 on 2021-09-19 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_userarea_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userarea',
            name='designation',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='userarea',
            name='position',
            field=models.CharField(max_length=45, null=True),
        ),
    ]