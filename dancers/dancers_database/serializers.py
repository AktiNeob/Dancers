from rest_framework import serializers
from .models import DancersDataBase


class DancersDataBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DancersDataBase
        fields = '__all__' 