# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from .serializers import CompetitionDataBaseSerializer as cds

from .models import CompetitionDataBase as cd
from .models import Programs as pg

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

from django.views.generic import View

class BaseMethods(View):
    def get_request_data(self, request):
        return request[data]



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



class BaseCreateNewCompetition(BaseMethods):
    
    def data_analizer(self, request_data):
        programs = request_data["programs"]
        request_data.pop("programs")
        competition = request_data
        return competition, programs
    
    def create_new_competition(self, competition):
        new_competition = cd.objects.create(
            name = competition["name"],
            date = competition["date"],
            rang = competition["rang"],
            start_registration = competition["start_registration"],
            online_registration = competition["online_registration"],
            organizer = competition["organizer"],
            location = competition["location"]
        )
        return new_competition

    def create_competitions_programs(self, new_competition, programs):
        for program in range(0, len(programs)):
            new_program = pg.objects.create(
                program = program["program"],
                age_groups = program["age_groups"],
                class_groups = program["class_groups"]
            )
    
    def manager(self, request):
        request_data = self.get_request_data(request)
        competition, programs = self.data_analizer(request_data)
        new_competition = self.create_new_competition(competition)
        self.create_competitions_programs(new_competition, programs)
"""
    {   
        "name": "",
        "date": "",
        rang: "",
        start_registration: "",
        end_registration: "",
        online_registration: "",
        organizer: "",
        location: "",
        programs: [
            {
            referees: "",
            program: "",
            age_groups: "",
            class_groups: ""
            },

            {
            referees: "",
            program: "",
            age_groups: "",
            class_groups: ""
            }
        ]
    }
"""

class CreateNewCompetition(BaseCreateNewCompetition):
    
    def post(self, request):
        self.manager(request)
        return JsonResponse({}, status=201)