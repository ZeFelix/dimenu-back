from django.shortcuts import render
from api.models import *
from api.serializers import ClientSerializer, OwnerSerializer, EmployeeSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



class UserDetail(APIView):
    """
    Classe que verificar qual tipo de usuário é
    """

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (JWTAuthentication,) 

    def get(self, requesy, pk):
        user = User.objects.get(pk=pk)
        try:
            client = user.client
            serializer = ClientSerializer(client)
            data = serializer.data
            data["user_type"] = "client"
            return Response(data)

        except ObjectDoesNotExist:
            
            try:
                employee = user.employee
                serializer = EmployeeSerializer(employee)
                data = serializer.data
                data["user_type"] = "employee"
                return Response(data)
            except ObjectDoesNotExist:
                owner = user.owner
                serializer = OwnerSerializer(owner)
                data = serializer.data
                data["user_type"] = "owner"
                return Response(data)