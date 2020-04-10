# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class CompetitionDataBase(models.Model):
    uuid = 

    date = 
    rang = 

    start_registration =
    end_registration =  
    online_registration = 

    organizer =
    location = 
    
class Programs(models.Model):
    uuid
    program =
    age_groups = 
    class_groups = 

class Referees(models.Model):
    uuid 

class Dansers(models.Model):
    uuid

class Stages(models.Model):
    uuid
    stage_name


class Results(models.model):
    pass