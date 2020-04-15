# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from .serializers import CompetitionDataBaseSerializer as cds
from .models import CompetitionDataBase as cd
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

# Create your views here.

class BaseMethods(APIView):
    pass



class BaseCompetition(BaseMethods):
    pass

class Competitions(BaseCompetition):
    
    def get(self, request):
        
        competitions = cd.objects.all()
        serializer = cds(competitions, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):

        new_competition = request.data
        serializer = cds(data=dancer)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(status = status.HTTP_201_CREATED)
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class Competition(BaseCompetition):

    def get(self, request, uuid):

        try:
            competition = cd.objects.get(pk = uuid)
            serializer = cds(instance = competition)
            return Response(serializer.data)
            
        except DancersDataBase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        
        competition = cd.objects.get(pk = uuid)
        serializer = cds(instance = competition, data = request.data, partial = True)
        try:
            if serializer.is_valid():
                    serializer.save()
                    return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        except AssertionError:
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):

        competition = cd.objects.get(pk = uuid)
        competition.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)