from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
from django.db.models import Q
import threading
# from .utils import cartData, check_transaction, check_instalment
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .models import *
import secrets
import string



# from dateutil.relativedelta import *
from django.contrib.auth import (
    authenticate,
    logout as django_logout,
    login as django_login,
)
from django.shortcuts import render, redirect
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core import serializers
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta
import json
from django.contrib import messages
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
import os
import csv
from twilio.rest import Client

def send_message(first_name,last_name,my_phone):
    account_sid = 'AC9b7bd1cce238df5d7be12ec04217b4de'
    auth_token = 'fc565c56aeca87708e18998e77d982fa'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                            body=f'Mwaramutse , \n \n Twabibutsa ga yuko {first_name} {last_name} agomba kuza gufata urukingo mu minsi itatu iri imbere ',
                            from_='+18609578207',
                            to=f'+25{my_phone}' 
                            )

#User

class registerRec(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        print(request.data)
        try:
            user1 = User.objects.get(email=request.data["email"])
            response = {
                "status": "Failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "A user with that email already exists!",
                "data": [],
            }

            return Response(response)
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.data["phone"])
                response = {
                    "status": "Failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "A user with that phone number already exists!",
                    "data": [],
                }

                return Response(response)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.data["FirstName"],
                    LastName='-',
                    DOB=None,
                    typee='Recipient',
                    email=request.data["email"],
                    phone=request.data["phone"],
                    password=request.data["password"],
                )
                response = {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Kwiyandikisha byagenze neza!!!",
                    "data": [],
                }

                return Response(response)


class register(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        print(request.data)
        try:
            user1 = User.objects.get(email=request.data["email"])
            response = {
                "status": "Failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "A user with that email already exists!",
                "data": [],
            }

            return Response(response)
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.data["phone"])
                response = {
                    "status": "Failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "A user with that phone number already exists!",
                    "data": [],
                }

                return Response(response)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.data["FirstName"],
                    LastName=request.data["LastName"],
                    Place=request.data["Place"],
                    Btype=request.data["Btype"],
                    typee=request.data["typee"],
                    DOB=request.data["DOB"],
                    typee='Donor',
                    email=request.data["email"],
                    phone=request.data["phone"],
                    password=request.data["password"],
                )
                response = {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Kwiyandikisha byagenze neza!!!",
                    "data": [],
                }

                return Response(response)


def user_login(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(phone=body["phone"])
            if user.check_password(body["password"]):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "user_type": user.typee,
                    "status": "success",
                    "token": str(token),
                    "code": status.HTTP_200_OK,
                    "message": "Kwinjira byagenze neza",
                    "data": [],
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json")
            else:
                data = {
                    "status": "failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Phone or password incorrect!",
                    "data": [],
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json")
        except User.DoesNotExist:
            data = {
                "status": "failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Phone or password incorrect!",
                "data": [],
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type="application/json")          


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"


class GetuserbyId(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['user_id'])

#Request

class Requestbyuserid(ListAPIView):
    serializer_class = RequestSerializer
    def get_queryset(self):
        return Request.objects.filter(user=self.kwargs['user_id'])


class RequestCreateView(CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestListView(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestUpdateView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    lookup_field = "id"

