from django.shortcuts import render
from api.models import Table
from api.serializers import TableSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class TableList(APIView):
    def get(self, request, company_id):
        tables = Table.objects.filter(company = company_id)
        serializer = TableSerializer(tables, many = True)
        return Response(serializer.data)

    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail': 'ID must be greater than zero'}, status = status.HTTP_400_BAD_REQUEST)
            request.data['company'] = company_id
            serializer = TableSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            return JsonResponse({'detail': 'An error ocurred on the server'+str(a)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


class TableDetail(APIView):
    def get_object(self, company_id, pk):
        try:
            return Table.objects.get(company = company_id, pk = pk)
        except Table.DoesNotExist:
            raise Http404
    
    def get(self, request, company_id, pk):
        table = self.get_object(company_id, pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    def put(self, request, company_id, pk):
        table = self.get_object(company_id, pk)
        request.data['company'] = company_id
        serializer = TableSerializer(table, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, pk):
        table = self.get_object(company_id, pk)
        table.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)