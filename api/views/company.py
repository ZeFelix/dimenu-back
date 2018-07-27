from django.shortcuts import render
from api.models import *
from api.serializers import CompanySerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


# Create your views here.

class CompanyList(APIView):
    """
    Lista todas as empresas, cria uma nova empresa.
    * requerido autenticação
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Company.objects.all()

    def get(self, request, format = None):
        serializer = CompanySerializer(self.get_queryset(), many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = CompanySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    


class CompanyDetail(APIView):
    """
    View para acessar atributos via id da empresa
    * requerido permissão de acesso e autenticaçã do usuário
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Company.objects.all()


    def get_object(self, pk):
        try:
            return Company.objects.get(pk = pk)
        except Company.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format = None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)    

    def put(self, request, pk, format = None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        try:
            company = self.get_object(pk)
            company.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as o:
            return JsonResponse({'Detail':'Object not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        

