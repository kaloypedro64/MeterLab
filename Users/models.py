from django.db import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

# Create your models here.

class userarea(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        User, db_column='userid', related_name='userarea', on_delete=models.CASCADE)
    area = models.CharField(max_length=25, null=False)
    designation = models.CharField(max_length=45, null=True)
    user = models.CharField(max_length=45, null=True)
    up = models.CharField(max_length=145, null=True)

    class Meta:
        db_table = "auth_user_area"
