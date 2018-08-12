from django.shortcuts import render
from api.models import *
from api.serializers import CustomUserSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#exceptions
from django.core.exceptions import ObjectDoesNotExist
#encryptografia
from django.contrib.auth.hashers import make_password

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import Group

class CustomUserRegister(APIView):
    """
    View para cadastro de usuário owner (dono da empresa) ou usuário mobile
    is_client = True -> owner 
    is_client = False -> cliente mobile
    """
    
    def post(self, request):
        try:

            if not request.data["is_client"]:
                group_owner_ids = list(Group.objects.filter(name="owner").values_list('id', flat=True))
                request.data["is_owner"] = True
                request.data["groups"] = group_owner_ids
            else:
                group_mobile_ids = list(Group.objects.filter(name="mobile").values_list('id', flat=True))
                request.data["is_owner"] = False
                request.data["groups"] = group_mobile_ids
            
            request.data["company"] = None

            request.data["password"] = make_password(password=request.data["password"])
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomUserList(APIView):
    """
    Cria e lista todos os usuário de uma companhia
    requer autenticação e permissão
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            request.data["company"] = company_id
            request.data["password"] = make_password(password=request.data["password"])
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, company_id):

        try:
            if company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            users = CustomUser.objects.filter(company__id=company_id)
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class CustomUserDetail(APIView):
    """
    get, put and delete a Custom User by pk of a company
    * requerido permissões e autenticação do usuário
    """
    
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return CustomUser.objects.all()

    def get (self, request, company_id,pk):
        try:
            if pk == '0' or company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.get(company__id=company_id,pk=pk)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist as a:
            return JsonResponse({'user':'Does not exist!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put (self,request,company_id,pk):
        try:
            if pk == '0' or company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)            
            user = CustomUser.objects.filter(company__id=company_id).get(pk=pk)
            request.data['company'] = company_id
            
            """ 
            Verifica se existe a chave password:
                Verifica se o password é nulo se for remove para não mudar a senha atual 
                se não for nulo encripgrafica a nova senha para ser atualizada 
            """ 
            if 'password' in request.data and request.data['password'] == None: 
                del request.data['password'] 
            elif 'password' in request.data: 
                request.data['password'] = make_password(request.data['password']) 

            serializer = CustomUserSerializer(user,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as a:
            return JsonResponse({'detail':'User does not exist!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete (self, request, company_id,pk):
        try:
            if pk == '0' or company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)            
            user = CustomUser.objects.filter(company__id=company_id).get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as a:
            return JsonResponse({'detail':'User does not exist!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
