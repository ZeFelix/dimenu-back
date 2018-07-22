from django.shortcuts import render
from api.models import *
from api.serializers import AttributeSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class AttributeList(APIView):
    """
    Lista,cria todos os atributos dos produtos
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)


    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Attribute.objects.all()

    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail': 'ID must be greater than zero'}, status = status.HTTP_400_BAD_REQUEST)
            request.data['company'] = company_id
            serializer = AttributeSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            return JsonResponse({'detail': 'An error ocurred on the server'+str(a)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, company_id):
        attributes = Attribute.objects.filter(company_id= company_id)
        serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)

class AttributeDetail(APIView):
    """
    Atualiza, deleta e busca apenas um atributo
    """ 
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Attribute.objects.all()


    def get_object(self, company_id, pk):
        try:
            return Attribute.objects.get(company = company_id, pk = pk)
        except Attribute.DoesNotExist:
            raise Http404

    def get(self, request, company_id, pk):
        attribute = self.get_object(company_id, pk)
        serializer = AttributeSerializer(attribute)
        return Response(serializer.data)

    def patch(self, request, company_id, pk):
        attribute = self.get_object(company_id, pk)
        request.data['company'] = company_id
        serializer = AttributeSerializer(attribute, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, company_id, pk):
        attribute = self.get_object(company_id, pk)
        request.data['company'] = company_id
        serializer = AttributeSerializer(attribute, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, pk):
        attribute = self.get_object(company_id, pk)
        attribute.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)