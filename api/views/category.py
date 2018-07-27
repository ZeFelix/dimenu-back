from django.shortcuts import render
from api.models import *
from api.serializers import CategorySerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class CategoryList(APIView):
    """
    Lista,cria todos as Categorias
    * requerido permissão de acesso e autenticaçã do usuário
    """
    
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Category.objects.all()

    def get(self, request, company_id, format = None):
        categories = Category.objects.filter(company = company_id)
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)

    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail': 'ID must be greater than zero'}, status = status.HTTP_400_BAD_REQUEST)
            request.data['company'] = company_id
            serializer = CategorySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print(a)
            return JsonResponse({'detail': 'An error ocurred on the server'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetail(APIView):
    """
    Edita, deleta e detalha uma Categoria
    * requerido permissão de acesso e autenticaçã do usuário
    """
    
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Category.objects.all()

    def get_object(self, company_id, pk):
        try:
            return Category.objects.get(company = company_id, pk = pk)
        except Category.DoesNotExist:
            raise Http404
            
    def get(self, request, company_id, pk):
        category = self.get_object(company_id, pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, company_id, pk):
        if pk == '0' or company_id == '0':
            return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        category = self.get_object(company_id, pk)
        request.data["company"] = company_id
        serializer = CategorySerializer(category, data = request.data, partial=True)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, pk):
        category = self.get_object(company_id, pk)
        category.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)