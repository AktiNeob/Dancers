from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from .serializers import DancersDataBaseSerializer
from .models import DancersDataBase
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
import traceback

import logging
logger = logging.getLogger('danceLog')
validLogger = logging.getLogger("validlogger")

class BaseView(APIView):
    
    def dancerLogger(self, request, response, errors = [], uuid = 0):

        if request.method == "GET":

            if uuid == 0:
                logger.info(
                    f'{request.method} - {request.build_absolute_uri()}\n{request.GET}\nResponse: {response}')
            else:
                logger.info(
                    f'{request.method} - {request.build_absolute_uri()}\n{request.GET}\nUUID: {uuid}\nResponse: {response}')
            

        elif request.method == "POST":
            
            FieldValidMessage = []
            for i in errors:
                FieldValidMessage.append(f"{i}: {errors[i][0]}") 
            errors = "\n".join(FieldValidMessage)

            logger.info(
                f'{request.method} - {request.build_absolute_uri()}\n\nData:\n{request.data}\n\nResponse: {response}\n\nProblems:\n{errors}')
        
        elif request.method == "PATCH":
            
            FieldValidMessage = []
            for i in errors:
                FieldValidMessage.append(f"{i}: {errors[i][0]}") 
            errors = "\n".join(FieldValidMessage)

            logger.info(
                f'{request.method} - {request.build_absolute_uri()}\n\nData:\n{request.data}\n\nUUID: {uuid}\nResponse: {response}\n\nProblems:\n{errors}')

        if request.method == "DELETE":
          
            logger.info(
                f'{request.method} - {request.build_absolute_uri()}\n{request.GET}\nUUID: {uuid}\nResponse: {response}')
        
    
class DancersView(BaseView):

    def get(self, request):
        
        dancers = DancersDataBase.objects.all()
        serializer = DancersDataBaseSerializer(dancers, many=True)
        self.dancerLogger(request = request, response = "HTTP_200_OK")
        return Response(data = serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):

        dancer = request.data
        serializer = DancersDataBaseSerializer(data=dancer)
        try:
            if serializer.is_valid():
                serializer.save()
                self.dancerLogger(request = request, response = "HTTP_201_CREATED")
                return Response(status = status.HTTP_201_CREATED)
        except:
            self.dancerLogger(request = request, response = "HTTP_400_BAD_REQUEST", errors = serializer.errors)
            return Response(status = status.HTTP_400_BAD_REQUEST)
    
class DancerView(BaseView):

    def get(self, request, uuid):
        try:
            dancer = DancersDataBase.objects.get(pk = uuid)
            serializer = DancersDataBaseSerializer(instance = dancer)
            self.dancerLogger(request = request, response = "HTTP_200_OK", uuid = uuid)
            return Response(serializer.data)
            
        except DancersDataBase.DoesNotExist:
            self.dancerLogger(request = request, response = "HTTP_404_NOT_FOUND", uuid = uuid)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        
        dancer = DancersDataBase.objects.get(pk = uuid)
        serializer = DancersDataBaseSerializer(instance = dancer, data = request.data, partial = True)
        try:
            if serializer.is_valid():
                    serializer.save()
                    self.dancerLogger(request = request, response = "HTTP_202_ACCEPTED", uuid = uuid)
                    return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)
        except AssertionError:
            self.dancerLogger(request = request, response = "HTTP_400_BAD_REQUEST", errors = serializer.errors, uuid = uuid)
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        dancer = DancersDataBase.objects.get(pk = uuid)
        dancer.delete()
        self.dancerLogger(request = request, response = "HTTP_204_NO_CONTENT", uuid = uuid)
        return Response(status = status.HTTP_204_NO_CONTENT)
    
def print_page(request):
    
    return render(request,'dancers_database/index.html')
    
def print_data(request):
    print(request.method)
    print(request.POST)
    print(status)
    print(status.HTTP_200_OK)
    print(123)

    r = JsonResponse({"111": "222"})
    print(r)
    return r