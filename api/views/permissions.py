from django.shortcuts import render
from django.contrib.auth.models import Permission, Group
from api.serializers import PermissionSerializer, GroupSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class PermissionList(APIView):
    """
    List all Permissions
    * requerido permissões e autenticação do usuário
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        permissions = Permission.objects.filter(content_type__app_label='api')
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PermissionDetail(APIView):
    """
    List a permission details
    * requerido permissões e autenticação do usuário
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get(self, request, pk):
        try:
            permission = Permission.objects.get(pk=pk)
            serializer = PermissionSerializer(permission)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as o:
            return Response({"Detail":"Object not exist!"},status=status.HTTP_400_BAD_REQUEST)
        

class GroupList(APIView):
    """
    List all groups
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    
    def  get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
            

class GroupDetail(APIView):
    """
    list a groups details
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    
    def get(self, request, pk):
        try:
            permission = Group.objects.get(pk=pk)
            serializer = GroupSerializer(permission)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as o:
            return Response({"Detail":"Object not exist!"},status=status.HTTP_400_BAD_REQUEST)
        
