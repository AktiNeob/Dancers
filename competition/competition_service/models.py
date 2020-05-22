# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from uuid import uuid4


# Базовая Модель
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4)

    class Meta:
        abstract = True


# Модель Совернований
class CompetitionDataBase(BaseModel):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    rang = models.CharField(max_length=50)

    start_registration = models.CharField(max_length=50)
    end_registration =  models.CharField(max_length=50)
    online_registration = models.BooleanField(default=False)

    organizer = models.CharField(max_length=50)
    location =  models.CharField(max_length=50)
    

# Судьи соревнований
class Referees(BaseModel):
    referee_uuid = models.UUIDField()


# участники соревнований
class Dansers(BaseModel):
    dancers_uuid = models.UUIDField()


# Программы соревнований
class Programs(BaseModel):
    competition  = models.ForeignKey(CompetitionDataBase, on_delete=models.CASCADE)

    referees = models.ManyToManyField(Referees)
    members = models.ManyToManyField(Dansers)

    program = models.CharField(max_length=100)
    age_groups = models.CharField(max_length=100)
    class_groups = models.CharField(max_length=100)


# Этапы программ соревнований
class Stages(BaseModel):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    members = models.ManyToManyField(Dansers)
    program = models.CharField(max_length=50)
    stage_name = models.CharField(max_length=50)