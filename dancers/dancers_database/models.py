from django.db import models
from uuid import uuid4
from .validators import refereeValid, classValid, sportValid, genderValid, trainerValid

# Create your models here.

class DancersDataBase(models.Model):

    uuid = models.UUIDField(primary_key = True, default = uuid4)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, validators=[genderValid])
    #date_of_birth = models.DateField()
    club = models.CharField(max_length=50)   # Должен валидироваться со списком зареганных клубов при добавлени спортсмена

    points_in_E_class = models.SmallIntegerField()
    points_in_D_class = models.SmallIntegerField()
    points_in_C_class = models.SmallIntegerField()
    points_in_B_class = models.SmallIntegerField()
    points_in_A_class = models.SmallIntegerField()
    points_in_S_class = models.SmallIntegerField()
    points_in_M_class = models.SmallIntegerField()
    
    trainer_rank = models.CharField(max_length=50, validators=[trainerValid] )
    referee_rank = models.CharField(max_length=50, validators=[refereeValid])
    sport_rank = models.CharField(max_length=50, validators=[sportValid])
    class_rank = models.CharField(max_length=3, validators=[classValid])

   