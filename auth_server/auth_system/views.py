from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse, request

from .serializers import ServiceSessionsSerializer, UsersDataBaseSerializer, UsersDataBaseSerializer, UsersSessionsSerializer

from .models import ServiceSessions as ss
from .models import UsersDataBase as ud
from .models import UsersSessions as us

import datetime
import secrets
import re

from django.conf import settings

import os
os.system("clear")

import hashlib

import logging
auth_logger = logging.getLogger('auth_log')


#Методы, используемые во всех классах
class BaseMethods(APIView):
    
    def get_request_data(self, request):
            
            data = request.data      
            return data

    def token_verification(self, request_data: dict, model, token_type: str, token_ttl: datetime) -> dict:

        token = request_data[token_type]

        try:
            if token_type == "access_token":
                entry = model.objects.get(access_token = token)

            else:
                entry = model.objects.get(refresh_token = token)
        except:
            return {"message": "Bad Token"}
        
        token_born_time = entry.token_born
        token_born_time = datetime.datetime.strptime(token_born_time, '%d/%m/%y %H:%M:%S')
        
        token_end_of_life = token_born_time + token_ttl
        now = datetime.datetime.now()

        if now > token_end_of_life:
            return {"message": f"{token_type} is Dead", "entry": entry}

        else:
            return {"message": "Success", 'entry': entry}

    def create_tokens(self, access_token_ttl: datetime, refresh_token_ttl: datetime, token_size: int, entry) -> dict: 

        access_token = secrets.token_urlsafe(token_size)
        refresh_token = secrets.token_urlsafe(token_size)

        now = datetime.datetime.now()
        token_born = now.strftime("%d/%m/%y %H:%M:%S")

        access_token_valid_until = now + access_token_ttl
        access_token_valid_until = access_token_valid_until.strftime("%d/%m/%y %H:%M:%S")

        refresh_token_valid_until = now + refresh_token_ttl
        refresh_token_valid_until = refresh_token_valid_until.strftime("%d/%m/%y %H:%M:%S")

        entry.access_token = access_token
        entry.refresh_token = refresh_token
        entry.token_born = token_born
        entry.save()

        return {
                "access_token": access_token, 
                "refresh_token": refresh_token,
                "access_token_valid_until": access_token_valid_until, 
                "refresh_token_valid_until": refresh_token_valid_until
                }

    def role_verifications(self, session, request_data: dict) -> dict:
        
        access_roles = request_data['access_roles'].split(",")
        user_uuid = session.user_uuid
        user = ud.objects.get(pk=user_uuid)

        users_roles = user.role
        users_roles = users_roles.split(',')

        for user_role in users_roles:
            if user_role in access_roles:
                return {"message": "Access is allowed"}
                break
        return {"message": "No Access"}

 
  
        pass

    def hash_password(self, password):

        h = hashlib.md5(password.encode())
        result = h.hexdigest()
        return result
    
    @staticmethod
    def authorization(roles):
        def user_auth_decorator(func):
            def wrapper(*args, **kwargs):
                if 'Authorization' in args[1].headers:
                    access_token = args[1].headers['Authorization']
                    try:
                        session = us.objects.get(access_token = access_token)
                    except:
                        return JsonResponse({"message": "Отказано в доступе"})
                    # TODO Добавить верификацию токена
                    user = ud.objects.get(pk=session.user_uuid)
                    if user.role in roles:
                        return func(*args, **kwargs)
                    else:
                        return JsonResponse({"message": "Отказано в доступе"})

                else:
                    return JsonResponse({"message": "Требуется авторизация"})
                # print(dir(args[1].data))
            
                
            return wrapper
        return user_auth_decorator


# Классы для работы с WhiteList сервисов
class ApiWhiteListBase(BaseMethods):

    apps = settings.APP_CREDITALES

    # Функция логирования класса WhiteList. Основные настройки логгера лежат в settings.py
    def logger(self, request, response, uuid=0, erros = []):

        if request.method == "GET":
            if uuid == 0:
                auth_logger.info( 
                    f'\nУправление WhiteList Межсервисной Авторизации\n{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')
            else:
                auth_logger.info(
                    f'{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nUUID: {uuid}\n\nResponse: {response}')
        
        elif request.method == "POST":
            auth_logger.info( 
                f'{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')

        elif request.method == "DELETE":
          
            auth_logger.info(
                f'{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nUUID: {uuid}\n\nResponse: {response}')

    # Функция валидации 
    def validator(self, data):
        if data["app_id_1"] == data["app_id_2"]:
            return {"message": "ОШИБКА: app_id_1 не дожен быть равен app_id_2"}
        
        app_id_1 = data["app_id_1"]
        app_id_2 = data["app_id_2"]

        if (not app_id_1 in self.apps) or (not app_id_2 in self.apps):
            return {"message": "Незарегистрированные сервисы"}

        try:
            entry = ss.objects.get(app_id_1 = app_id_1, app_id_2 = app_id_2)
            return {"message": "ОШИБКА: Запись уже существует"}
        except:
            return {"message": "Success"}

class ApiWhiteList(ApiWhiteListBase):

    # @BaseMethods.authorization('SuperVisor') 
    def get(self, request):
        users = ss.objects.all()
        serializer = ServiceSessionsSerializer(users, many=True)
        self.logger(request = request, response = "HTTP_200_OK")
        return Response(data = serializer.data, status=status.HTTP_200_OK)

    # @BaseMethods.authorization('SuperVisor')
    def post(self, request):
        new_entry = request.data
        validator_status = self.validator(new_entry)
        if validator_status["message"] != "Success":
            status_ = validator_status["message"]
            self.logger(request = request, response = f"HTTP_400_BAD_REQUEST\n{status_}")
            return JsonResponse({"message": validator_status["message"]}, status=400)
        serializer = ServiceSessionsSerializer(data=new_entry)
        try:
            if serializer.is_valid():
                serializer.save()
                self.logger(request = request, response = "HTTP_201_CREATED")
                return Response(status = status.HTTP_201_CREATED)
        except:
            self.logger(request = request, response = "HTTP_400_BAD_REQUEST")
            return Response(status = status.HTTP_400_BAD_REQUEST)

class ApiWhiteListEntry(ApiWhiteListBase):

    # @BaseMethods.authorization('SuperVisor')
    def get(self, request, uuid):
        try:
            entry = ss.objects.get(pk = uuid)
            serializer = ServiceSessionsSerializer(instance = entry)
            self.logger(request = request, response = "HTTP_200_OK", uuid=uuid)
            return Response(serializer.data)
            
        except ss.DoesNotExist:
            self.whitelist_logger(request = request, response = "HTTP_404_NOT_FOUND", uuid=uuid)
            return Response(status=status.HTTP_404_NOT_FOUND)

    # @BaseMethods.authorization('SuperVisor')
    def delete(self, request, uuid):
        dancer = ss.objects.get(pk = uuid)
        dancer.delete()
        self.logger(request = request, response = "HTTP_204_NO_CONTENT", uuid=uuid)
        return Response(status = status.HTTP_204_NO_CONTENT) 


# Классы для работы с Межсервисной авторизацией
class BaseServiceAuthMethods(BaseMethods):

    access_token_ttl = settings.SERVICE_ACCESS_TOKEN_TTL
    refresh_token_ttl = settings.SERVICE_REFRESH_TOKEN_TTL
    token_size = settings.SERVICE_TOKEN_SIZE
    app_creds = settings.APP_CREDITALES 

    def logger(self, request, response, ):
        auth_logger.info( 
                    f'\nМежсервисная Авторизация\n{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')
           
    def white_list_verification(self, request_data, status):

        if status == "First Auth":
            try:
                white_list_entry = ss.objects.get(app_id_1 = request_data['app_id_1'], app_id_2 = request_data['app_id_2'])
                return {"message": "Success", "entry": white_list_entry}
            except:
                return {"message": "No Access"}

        elif status == "Token Update":
            try:
                white_list_entry = ss.objects.get(refresh_token = request_data['refresh_token'])
                return {"message": "Success", "entry": white_list_entry}
            except:
                return {"message": "No Access"}

        elif status == "Auth":
            try:
                white_list_entry = ss.objects.get(access_token = request_data['access_token'])
                return {"message": "Success", "entry": white_list_entry}
            except:
                return {"message": "No Access"}
        
    def data_analizator(self, request_data):
        
        if ('app_id_1' in request_data) and ('app_id_2' in request_data) and ('app_secret' in request_data) :
            return "First Auth"

        elif "access_token" in request_data:
            return "Auth"

        elif "refresh_token" in request_data:
            return "Token Update"

        else:
            return "BAD Request"

    def appid_verification(self, request_data):

        valid_secret = self.app_creds[request_data['app_id_1']]
        if valid_secret != request_data['app_secret']:
            return {"message": "No Access"}
        else:
            return {"message": "Success"}
        
    def Auth(self, request):

        access_token_ttl = settings.SERVICE_ACCESS_TOKEN_TTL
        refresh_token_ttl = settings.SERVICE_REFRESH_TOKEN_TTL 

        request_data = self.get_request_data(request)
        status = self.data_analizator(request_data)
        print(status)

        if status == "BAD Request":
            return {"message": 'Bad Request', "status": 400}
        
        white_list_entry = self.white_list_verification(request_data, status)
        if white_list_entry["message"] == "No Access":
            return {"message": "No Access", "status": 400}
        
        if status == "First Auth":
            appid_status = self.appid_verification(request_data)
            if appid_status["message"] == "Success":
                tokens = self.create_tokens(self.access_token_ttl, self.refresh_token_ttl, 32, white_list_entry["entry"])
                return {'data': tokens, "status": 200}
            else:
                return {"message": appid_status["message"], "status": 400}


        if status == "Token Update":
            token_status = self.token_verification(request_data, ss, "refresh_token", refresh_token_ttl)
            if token_status["message"] == 'Success':
                tokens = self.create_tokens(self.access_token_ttl, self.refresh_token_ttl, 32, white_list_entry["entry"])
                return {'data': tokens, "status": 200}
            else:
                print(token_status["message"])
                return {"message": token_status["message"], "status": 400}


        if status == "Auth":
            access_token_status = self.token_verification(request_data, ss, "access_token", self.refresh_token_ttl)
            if access_token_status["message"] == 'Success':
                return {"message": access_token_status["message"], "status": 200}
            else:
                return {"message": access_token_status["message"], "status": 400}

class ServiseAuth(BaseServiceAuthMethods):
    
    def post(self, request):
        response_data = self.Auth(request)
        print(response_data)
        status = response_data["status"]
        self.logger(request, f'{status}')
        if "data" in response_data:
            return JsonResponse(response_data["data"], status=response_data["status"])
        else:
            return JsonResponse({"message": response_data["message"]}, status=response_data["status"])


# Классы для работы с Авторизацией пользователей 
class BaseUsersAuthorization(BaseMethods):

    access_token_ttl = settings.USER_ACCESS_TOKEN_TTL
    refresh_token_ttl = settings.USER_REFRESH_TOKEN_TTL 
    token_size = settings.USER_TOKEN_SIZE
    
    def logger(self, request, response):
        auth_logger.info( 
                f'\nАвторизация Пользователя\n{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')
           
    def data_analizator(self, request_data):
        
        if 'access_token' in request_data and 'access_roles' in request_data:
            return {"message": "Authorization"}
        else:
            return {"message": "Bad Request"}

    def user_authorization_controller(self, request):

        request_data = self.get_request_data(request)
        data_status = self.data_analizator(request_data)

        if data_status["message"] == "Authorization":
            token_verification_status = self.token_verification(request_data, us, "access_token", self.access_token_ttl)
            if token_verification_status["message"] == "Success":
                role_verification_status = self.role_verifications(token_verification_status["entry"], request_data)
                return {"data": role_verification_status["message"], "status": 200}
            else:
                return {"data": token_verification_status["message"], "status": 400}
        else:
            return {"data": data_status["message"], "status": 400}

class UsersAuthorization(BaseUsersAuthorization):
    def post(self, request):

        authorization_status = self.user_authorization_controller(request)
        self.logger(request, f'{authorization_status}')
        return JsonResponse({"message": authorization_status["data"]}, status=authorization_status["status"])


# Классы для работы с Сессиями и Аутентификацией пользователей
class BaseUserSession(BaseMethods):

    access_token_ttl = settings.USER_ACCESS_TOKEN_TTL
    refresh_token_ttl = settings.USER_REFRESH_TOKEN_TTL
    token_size = settings.USER_TOKEN_SIZE

    def logger(self, request, response):
        auth_logger.info( 
                f'\nАвторизация Пользователя\n{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')
           
    def data_analizator(self, request_data):
        
        if ('login' in request_data) and ('password' in request_data):
            return  "NewSession"
        
        elif 'refresh_token' in request_data:
            return "UpdateSession"
        
        else:
            return "Bad Request"

    def authentication(self, request_data):
        
        login = request_data['login']
        password = request_data['password']

        h_password = self.hash_password(password)

        try:
            user = ud.objects.get(login=login)
        except:
            return {"message": "Неверный логин или пароль", 'entry': None}
        
        if user.password == h_password:
            return {"message": "Success", 'entry': user}
        else:
            return {"message": "Неверный логин или пароль", 'entry': None}

    def create_new_session(self, user):
        session = us(
                user_uuid = user.user_uuid,
            )
        session.save()
        return session

    def session_controller(self, request):
        
        request_data = self.get_request_data(request)
        data_status = self.data_analizator(request_data)
        
        if data_status == 'NewSession':
            authentication_status = self.authentication(request_data)

            if authentication_status['message'] == 'Success':
                user = authentication_status['entry']
                session = self.create_new_session(user)
                tokens = self.create_tokens(self.access_token_ttl, self.refresh_token_ttl, self.token_size, session)
                return tokens
            else:
                return {"message": authentication_status['message']}

        elif data_status == 'UpdateSession':
            token_status = self.token_verification(request_data, us, "refresh_token", self.refresh_token_ttl)
            print(token_status['message'])
            if token_status['message'] == "refresh_token is Dead":
                token_status['entry'].delete()
                return{"message": "Сессия удалена, так-как истек refresh token"}

            if token_status['message'] == 'Success':
                session = token_status['entry']
                tokens = self.create_tokens(self.access_token_ttl, self.refresh_token_ttl, self.token_size, session)
                return {
                    "access_token": tokens['access_token'], 
                    "refresh_token": tokens['refresh_token'],
                    "access_token_valid_until": tokens['access_token_valid_until'], 
                    "refresh_token_valid_until": tokens['refresh_token_valid_until']
                }
            else:
                return {"message": token_status['message']}
        else:
            return {"message": data_status}

class UserSessions(BaseUserSession):
    def post(self, request):
        session_status = self.session_controller(request)
        self.logger(request, f'{session_status}')
        return JsonResponse(session_status)


# Классы для работы с регистрацией пользователя
class BaseUserRegistration(BaseUserSession):

    error_messages = {}

    access_token_ttl = settings.USER_ACCESS_TOKEN_TTL
    refresh_token_ttl = settings.USER_REFRESH_TOKEN_TTL
    token_size = settings.USER_TOKEN_SIZE
    
    def logger(self, request, response):
        auth_logger.info( 
                f'\nОПЕРАЦИЯ: Cоздание Нового Пользователя\n{request.method} - {request.build_absolute_uri()}\n\nQuery Params\n{request.GET}\n\nHeaders\n{request.headers}\n\nData:\n{request.data}\n\nResponse: {response}')
 
    def validator(self, data, name):
        operation_error = False
        characherRegex = re.compile(r'[^a-zA-Z0-9.]')
        if len(data) < 5:
            operation_error = True
            self.error_messages[name] = f"{name} должен содержать не менее 5 символов"
         
        symbol_valid = characherRegex.search(data)
        if bool(symbol_valid):
            if operation_error == True:
                self.error_messages[name] += ",Недопустимые символы"
            else:
                operation_error = True
                self.error_messages[name] = "Недопустимые символы"
        
        if name == 'login':
            pass
            try:
                user = ud.objects.get(login=data)
                self.error_messages[name] = "Имя уже используется"
                operation_error = True
            except:
                pass
        print()
        return operation_error      

    def data_analizator(self, request_data):
        data = {}
        if "login" in request_data and 'password' in request_data:
            data['login'] = request_data['login']
            data['password'] = request_data['password']
            return {"status": "Success", 'data': data}
        else:
            return {"status":"Bad Request"}

    def registration(self, request):
        request_data = self.get_request_data(request)
        data_status = self.data_analizator(request_data)
        if data_status["status"] == "Success":
            data = data_status['data']
            for key in data:
                validation_error = self.validator(data[key], key)
                if validation_error == True:
                    print(self.error_messages)
                    return {"data": self.error_messages, "status": 400}
    
            data = data_status['data']
            data['password'] = self.hash_password(data['password'])
            new_user = ud(login = data['login'], password = data['password'], role='sportsman')
            new_user.save()
            new_user = ud.objects.get(login = data['login'])
            session = self.create_new_session(new_user)
            tokens = self.create_tokens(self.access_token_ttl, self.refresh_token_ttl, self.token_size, session)
            return {'data': tokens, 'status': 201}
        else:
            return{"data": data_status["status"], "status": 400}

class UserRegistration(BaseUserRegistration):
    def post(self, request):
        user_status = self.registration(request)
        self.logger(request, user_status['status'])
        return JsonResponse(user_status["data"], status=user_status["status"])
    

# Классы для управления аккаунтами пользователей
class BaseAccountManagement(BaseMethods):
    
    available_roles = settings.AVAILABLE_ROLES
 
    def logger(self, rquest, response):
        pass

    def data_analizer(self, request_data):
        data = {}
        if "method" in request_data:
            if "role" in request_data and "login" in request_data:
                data["method"] = request_data["method"]
                data["login"] = request_data["login"]
                data["role"] = request_data["role"]
                return {"status": "Success", "data": data}
            else:
                return {"status": "Bad Request"}
        else:
            return {"status": "Bad Request"}

    def validator(self, data):
        if data['role'] in self.available_roles:
            return True
        else:
            return False
     
    # @BaseMethods.authorization('SuperVisor', 'admin')     
    def give_role(self, data):
        
        role_is_valid = self.validator(data)
        if not role_is_valid:
            return {"data": "роль введена не корректно", "status": 400}

        user = ud.objects.get(login=data['login'])

        roles = user.role
        roles = roles.split(",")
        if data['role'] in roles:
            return {"data": "Пользователь уже обладает указанной ролью", "status": 400}

        user.role += (',' + data['role'])
        user.save()
        role = data['role']
        login = data['login']
        return{'data': f'Роль {role} успешно добалена пользователю {login}', "status": 200}

    # @BaseMethods.authorization('SuperVisor', 'admin') 
    def take_away_role(self, data):
        role_is_valid = self.validator(data)
        if not role_is_valid:
            return {"data": "Данный пользователь не обладает указанной ролью", "status": 400}

        user = ud.objects.get(login=data['login'])
        roles = user.role.split(',')
        for i in range(0, len(roles)):
            if roles[i] == data['role']:
                roles.pop(i)
                user.role = ",".join(roles)
                user.save()
                role = data['role']
                login = data['login']
                return {'data': f'Роль {role} успешно удалена у пользователя {login}', "status": 204}
        return {"data": "Данный пользователь не обладает указанной ролью", "status": 400}

    def account_manager(self, request):
        request_data = self.get_request_data(request)
        data = self.data_analizer(request_data)
        if data["status"] == "Success":
            data = data["data"]
            if data['method'] == 'give_role':
                result = self.give_role(data)
                return result
            elif data['method'] == "take_away_role":
                result = self.take_away_role(data)
                return result
            else:
                return {"data": "Недопустимый метод", 'status': 400}
        else:
            return {"data": data["status"], 'status': 400}

class AccountManagement(BaseAccountManagement):
    def post(self, request):
        response = self.account_manager(request)
        return JsonResponse({"message": response["data"]}, status=response["status"])
    
