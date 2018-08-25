from django.shortcuts import render
from api.models import *
from api.serializers import IngredientSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.custom_permissions import CustomPermissions

class IngredientList(APIView):
    """
    Classe para lista todos os ingredientes e criar novos
    """

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Ingredient.objects.all()

    def get(self, request, company_id, format = None):
        ingredients = Ingredient.objects.filter(company = company_id)
        serializer = IngredientSerializer(ingredients, many = True)
        return Response(serializer.data)

    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail': 'ID must be greater than zero'}, status = status.HTTP_400_BAD_REQUEST)
            request.data['company'] = company_id
            serializer = IngredientSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            print(a)
            return JsonResponse({'detail': 'An error ocurred on the server'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class IngredientDetail(APIView):
    """
    Classe para listar detalhes de um ingredient, deletar e atualizar
    """
    
    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Ingredient.objects.all()

    def get_object(self, company_id, pk):
        try:
            return Ingredient.objects.get(company = company_id, pk = pk)
        except Ingredient.DoesNotExist:
            raise Http404
            
    def get(self, request, company_id, pk):
        ingredient = self.get_object(company_id, pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, company_id, pk):
        if pk == '0' or company_id == '0':
            return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        ingredient = self.get_object(company_id, pk)
        request.data["company"] = company_id
        serializer = IngredientSerializer(ingredient, data = request.data, partial=True)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, pk):
        ingredient = self.get_object(company_id, pk)
        ingredient.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)