from django.shortcuts import render
from api.models import *
from api.serializers import ProductSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProductList(APIView):
    """
    Lista e cria os produtos
    """

    def get(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            products = Product.objects.filter(company__id=company_id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as a:
            print (a)
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            request.data["company"] = company_id
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            return JsonResponse({"detail":"An error occurred on the server"+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductDetail(APIView):
    """
    Atualiza, deleta um produto
    """

    def get(self, request, company_id, pk):
        try:
            if pk == '0' or company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            product = Product.objects.get(company__id=company_id, pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except ObjectDoesNotExist as a:
            return JsonResponse({'detail':'Does not exist!'+str(a)},status=status.HTTP_204_NO_CONTENT)
        except Exception as a:
            return JsonResponse({"detail":"An error occurred on the server"+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def put(self, request, company_id, pk):
        if pk == '0' or company_id == '0':
            return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        product = Product.objects.get(company_id=company_id, pk=pk)
        request.data["company"] = company_id
        serializer = ProductSerializer(product, data = request.data, partial=True)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    def delete(self, request, company_id, pk):
        product = Product.objects.get(company_id=company_id, pk=pk)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
