# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from uuid import uuid4

# Create your models here.

class CompetitionDataBase(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4)

    date = models.CharField(max_length=50)
    rang = models.CharField(max_length=50)

    start_registration = models.CharField(max_length=50)
    end_registration =  models.CharField(max_length=50)
    online_registration = models.BooleanField(default=False)

    organizer = models.CharField(max_length=50)
    location =  models.CharField(max_length=50)
    
class Programs(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4)
    competition  = models.ForeignKey(CompetitionDataBase, on_delete=models.CASCADE)
    program = models.CharField(max_length=50)
    age_groups = models.CharField(max_length=50)
    class_groups = models.CharField(max_length=50)

# class Stages(models.Model):
#     uuid = models.UUIDField(primary_key = True, default = uuid4)
#     program = 
#     stage_name = 



# class Referees(models.Model):
#     uuid = models.UUIDField(primary_key = True, default = uuid4)
#     program = 
#     referee_uuid = models.UUIDField()

# class Dansers(models.Model):
#     uuid = models.UUIDField(primary_key = True, default = uuid4)
#     dancers_uuid


