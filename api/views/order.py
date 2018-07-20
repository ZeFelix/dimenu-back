from django.shortcuts import render
from api.models import *
from api.serializers import OrderSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class OrderList(APIView):
    
    def get(self, request, company_id):
        orders = Order.objects.filter(company_id=company_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, company_id):
        print(request.data)
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    
    def get(self, request, company_id, pk):
        try:
            if pk == '0' or company_id == '0':
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ObjectDoesNotExist as a:
            return JsonResponse({'detail':'Does not exist!'+str(a)},status=status.HTTP_204_NO_CONTENT)
        except Exception as a:
            return JsonResponse({"detail":"An error occurred on the server"+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, company_id, pk):
        try:
            order = Order.objects.get(company_id=company_id, pk=pk)
            serializer = OrderSerializer(order,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except expression as identifier:     
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, pk):
        try:
            order = Order.objects.get(company_id=company_id, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as o:
            return JsonResponse({'Detail':'Object not exist!'}, status=status.HTTP_400_BAD_REQUEST)
      