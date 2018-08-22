from django.shortcuts import render
from api.models import *
from api.serializers import OwnerSerializer
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
from api.custom_permissions import CustomPermissionsOwner

class RegisterOwner(APIView):
    """
    View para registrar os donos das empresas
    Não precisa autenticação
    """

    def post(self, request):

        try:
            group_owner_ids = list(Group.objects.filter(name="owner").values_list('id', flat=True)) 
            request.data["groups"] = group_owner_ids 
            request.data["password"] = make_password(password=request.data["password"]) 
            serializer = OwnerSerializer(data=request.data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OwnerDetail(APIView): 
    """ 
    get, put and delete a Owner by pk 
    * requerido permissões e autenticação do usuário 
    """ 
     
    permission_classes = (IsAuthenticated, DjangoModelPermissions, CustomPermissionsOwner,) 
    authentication_classes = (JWTAuthentication,) 
 
    def get_queryset(self): 
        """ 
        Metodo para verificar as permissões do usuário 
        """ 
        return Owner.objects.all() 
 
    def get (self, request,pk): 
        try: 
            if pk == '0': 
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST) 
            owner = Owner.objects.get(pk=pk) 
            serializer = OwnerSerializer(owner) 
            return Response(serializer.data) 
        except ObjectDoesNotExist as a: 
            return JsonResponse({'user':'Does not exist!'},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    def put (self,request,pk): 
        try: 
            if pk == '0': 
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)             
            owner = Owner.objects.get(pk=pk) 
             
            """  
            Verifica se existe a chave password: 
                Verifica se o password é nulo se for remove para não mudar a senha atual  
                se não for nulo encripgrafica a nova senha para ser atualizada  
            """  
            if 'password' in request.data and request.data['password'] == None:  
                del request.data['password']  
            elif 'password' in request.data:  
                request.data['password'] = make_password(request.data['password'])  
 
            serializer = OwnerSerializer(owner,data=request.data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data) 
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        except ObjectDoesNotExist as a: 
            return JsonResponse({'detail':'User does not exist!'},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    def delete (self, request,pk): 
        try: 
            if pk == '0': 
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)             
            owner = Owner.objects.get(pk=pk) 
            owner.delete() 
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except ObjectDoesNotExist as a: 
            return JsonResponse({'detail':'User does not exist!'},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
