from rest_framework import serializers
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'fantasy_name', 'cnpj', 'email', 'phone', 'qrcode_identification')