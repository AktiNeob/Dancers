from rest_framework import serializers
from .models import ServiceSessions, UsersDataBase, UsersSessions


class ServiceSessionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceSessions
        fields = '__all__' 

class UsersSessionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersSessions
        fields = '__all__' 

class UsersDataBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersDataBase
        fields = '__all__' 

