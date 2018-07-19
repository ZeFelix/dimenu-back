from django.shortcuts import render
from api.models import Avaliation
from api.serializers import AvaliationSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class AvaliationList(APIView):
    def get(self, request,  company_id):
        avaliations = Avaliation.objects.filter(company = company_id)
        serializer = AvaliationSerializer(avaliations, many = True)
        return Response(serializer.data)

    def post(self, request, company_id):
        try:
            if company_id == '0':
                return JsonResponse({'detail': 'ID must be greater than zero'}, status = status.HTTP_400_BAD_REQUEST)
            request.data['company'] = company_id
            serializer = AvaliationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            return JsonResponse({'detail': 'An error ocurred on the server'+str(a)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)