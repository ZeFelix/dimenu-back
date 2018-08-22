from django.shortcuts import render
from api.models import *
from api.serializers import EmployeeSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
#encryptografia 
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.models import Group 
from api.custom_permissions import CustomPermissionsEmployee

class EmployeeList(APIView):
    """
    Lista,cria todos os funcionários de uma empresa
    * requerido permissão de acesso e autenticaçã do usuário
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,CustomPermissionsEmployee,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Employee.objects.all()

    def post(self, request, company_id):

        try:
            group_employee_ids = list(Group.objects.filter(name="employee").values_list('id', flat=True)) 
            request.data["groups"] = group_employee_ids
            request.data["password"] = make_password(password=request.data["password"]) 
            serializer = EmployeeSerializer(data=request.data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, company_id):
        employees = Employee.objects.filter(company_id=company_id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class EmployeeDetail(APIView):
    """
    GET, PUT, DELETE employee
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,CustomPermissionsEmployee,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Employee.objects.all()

    def get(self, request, company_id, pk):
        employee = Employee.objects.get(company_id=company_id,pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self, request, company_id,pk, format = None):
        employee = Employee.objects.get(company_id=company_id,pk=pk)
        serializer = EmployeeSerializer(employee, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, pk, format = None):
        try:
            employee = Employee.objects.get(company_id=company_id,pk=pk)
            employee.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as o:
            return JsonResponse({'Detail':'Object not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        
