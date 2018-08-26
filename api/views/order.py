from django.shortcuts import render
from api.models import *
from api.serializers import OrderSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from api.custom_permissions import CustomPermissionsOrder, CustomPermissions, CustomPermissionsOrderTable
from cardapio import settings

class OrderList(APIView):
    """
    Lista todas os pedidos, cria um novo pedido.
    * requerido autenticação e permissão do usuário
    """
    
    permission_classes = (IsAuthenticated, DjangoModelPermissions,CustomPermissionsOrder,)
    authentication_classes = (JWTAuthentication,)
    
    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Order.objects.all()
    
    def get(self, request, company_id):
        """
        Verifica o token se é um client que ta fazendo a requisições de todas as ordes dele
        caso seja, filtra usando o company_id e o client
        """
        token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ","")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(pk=payload["user_id"])
            client = user.client
            orders = Order.objects.filter(company_id=company_id,client=client)
        except ObjectDoesNotExist:
            orders = Order.objects.filter(company_id=company_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"details":'Signature expired. Please log in again.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return JsonResponse({"details":'Invalid token. Please log in again.'}, status=status.HTTP_400_BAD_REQUEST) 

    
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, company_id):
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    """
    Atualiza, deleta e detalha uma compra.
    * requerido permissões e autenticação do usuário
    """
    
    permission_classes = (IsAuthenticated, DjangoModelPermissions,CustomPermissionsOrder,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Metodo para verificar as permissões do usuário
        """
        return Order.objects.all()
    
    def get(self, request, company_id, pk):
        try:
            if pk == '0' or company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            order = Order.objects.get(company_id=company_id,pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ObjectDoesNotExist as a:
            return JsonResponse({'detail':'Does not exist!'+str(a)},status=status.HTTP_204_NO_CONTENT)
        except Exception as a:
            return JsonResponse({"detail":"An error occurred on the server"+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, company_id, pk):
        try:
            request.data["company"] = company_id
            order = Order.objects.get(company_id=company_id, pk=pk)
            serializer = OrderSerializer(order,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as a:     
            return JsonResponse({"detail":"An error occurred on the server"+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, company_id, pk):
        try:
            order = Order.objects.get(company_id=company_id, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as o:
            return JsonResponse({'Detail':'Object not exist!'}, status=status.HTTP_400_BAD_REQUEST)


class OrderListTable(APIView):
    """
    Classe que lista todas as compras daquela mesa
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions,CustomPermissionsOrderTable,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return Order.objects.all()
    
    def get(self, request, company_id, pk):
        orders = Order.objects.filter(company=company_id, table=pk)
        serializers = OrderSerializer(orders, many=True)
        return Response(serializers.data)
    