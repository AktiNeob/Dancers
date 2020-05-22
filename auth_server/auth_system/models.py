from django.db import models
from uuid import uuid4

# Create your models here.

class ServiceSessions(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4)
    app_id_1 = models.CharField(max_length=50)
    app_id_2 = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100, null=True)
    refresh_token = models.CharField(max_length=100, null=True)
    token_born = models.CharField(max_length=100, null=True)


class UsersSessions(models.Model):
    session_uuid = models.UUIDField(primary_key = True, default = uuid4)
    user_uuid = models.UUIDField()
    access_token = models.CharField(max_length=100, null=True)
    refresh_token = models.CharField(max_length=100, null=True)
    token_born = models.CharField(max_length=100, null=True)

class UsersDataBase(models.Model):
    user_uuid = models.UUIDField(primary_key = True, default = uuid4)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    
