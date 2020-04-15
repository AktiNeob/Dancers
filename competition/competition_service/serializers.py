from rest_framework import serializers
from .models import CompetitionDataBase


class CompetitionDataBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitionDataBase
        fields = '__all__' 