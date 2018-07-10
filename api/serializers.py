from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import *
from django.contrib.auth.models import Permission, Group

# realiza as relações de muitos relacionamentos
from drf_writable_nested import WritableNestedModelSerializer

class GroupSerializer(serializers.ModelSerializer):
    """
    Grupo de permissões do django
    """
    class Meta:
        model = Group
        fields = ['id','name']

class PermissionSerializer(serializers.ModelSerializer):
    """
    Permissões do django
    """
    class Meta:
        model = Permission
        fields = ['id','name','codename']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'fantasy_name', 'cnpj', 'email', 'phone', 'qrcode_identification')
    
class CustomUserSerializer(WritableNestedModelSerializer):
    user_permissions = PermissionSerializer(many=True)
    groups = GroupSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ['id','password','username','first_name','email','cpf','phone','is_client','is_owner','company','is_staff','user_permissions','groups'] 
    password = serializers.CharField(write_only = True, required = False, allow_null = True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name', 'company']