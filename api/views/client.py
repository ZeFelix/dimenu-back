from api.custom_permissions import CustomPermissionsClient
from api.models import *
from api.serializers import AttributeSerializer, CategorySerializer, \
    ClientSerializer, CompanySerializer, IngredientSerializer, \
    ProductSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions, \
    IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterClient(APIView):
    """
    View para registrar os donos das empresas
    Não precisa autenticação
    """

    def post(self, request):

        try:
            group_client_ids = list(Group.objects.filter(name="client").values_list('id', flat=True)) 
            request.data["groups"] = group_client_ids
            request.data["password"] = make_password(password=request.data["password"]) 
            serializer = ClientSerializer(data=request.data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server: "+str(a)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientDetail(APIView): 
    """ 
    get, put and delete a Client by pk 
    * requerido permissões e autenticação do usuário 
    """ 
     
    permission_classes = (IsAuthenticated, DjangoModelPermissions,CustomPermissionsClient,) 
    authentication_classes = (JWTAuthentication,) 
 
    def get_queryset(self): 
        """ 
        Metodo para verificar as permissões do usuário 
        """ 
        return Client.objects.all() 
 
    def get (self, request,pk): 
        try: 
            if pk == '0': 
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST) 
            client = Client.objects.get(pk=pk) 
            serializer = ClientSerializer(client) 
            return Response(serializer.data) 
        except ObjectDoesNotExist as a: 
            return JsonResponse({'user':'Does not exist!'},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    def put (self,request,pk): 
        try: 
            if pk == '0': 
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)             
            client = Client.objects.get(pk=pk) 
             
            """  
            Verifica se existe a chave password: 
                Verifica se o password é nulo se for remove para não mudar a senha atual  
                se não for nulo encripgrafica a nova senha para ser atualizada  
            """  
            if 'password' in request.data and request.data['password'] == None:  
                del request.data['password']  
            elif 'password' in request.data:  
                request.data['password'] = make_password(request.data['password'])  
 
            serializer = ClientSerializer(client,data=request.data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data) 
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        except ObjectDoesNotExist as a: 
            return JsonResponse({'detail':'User does not exist!'},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    def delete (self, request,pk): 
        try: 
            if pk == '0': 
                return JsonResponse({'detail':'ID must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)             
            client = Client.objects.get(pk=pk) 
            client.delete() 
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except ObjectDoesNotExist as a: 
            return JsonResponse({'detail':'User does not exist!'},status=status.HTTP_400_BAD_REQUEST) 
        except Exception as a: 
            print (a) 
            return JsonResponse({"detail":"An error occurred on the server"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

"""""""""""""""""""""
Views para acesso livre do client
"""""""""""""""""""""

class ClientListCompanies(APIView):
    """
    Classe livre de autenticação para o cliente mobile visualizar as empresas
    """

    def get(self, request, format = None):
        try:
            city = request.GET["city"]
            companies = Company.objects.filter(city__iexact=city)
        except Exception:
            companies = Company.objects.all()
        serializer = CompanySerializer(companies, many = True)
        return Response(serializer.data)

class ClientListCategories(APIView):
    """
    Classe livre de autenticação para o cliente mobile visualizar as categorias de determinada empresa
    """

    def get(self, request, pk):
        categories = Category.objects.filter(company=pk)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ClientListProducts(APIView):
    """
    Classe livre de autenticação para o cliente mobile visualizar os produtos de determinada empresa
    """

    def get(self, request, pk):
        products = Product.objects.filter(company=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ClientListProductsByCategories(APIView):
    """
    Classe que lista todos os produtos daquela categoria
    """

    def get(self, request, pk, category_id):
        products = Product.objects.filter(category = category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ClientListAttributes(APIView):
    """
    Classe para visualizar os atributos daquela empresa que sejam adicionais
    """

    def  get(self, request, pk):
        attribute = Attribute.objects.filter(company=pk)
        serializer = AttributeSerializer(attribute, many=True)
        return Response(serializer.data)

class ClientListAttributesByProducts(APIView):
    """
    Classe para visualizar os atributos daquela empresa que sejam adicionais
    """

    def  get(self, request, pk, product_id):
        attribute = Attribute.objects.filter(product=product_id)
        serializer = AttributeSerializer(attribute, many=True)
        return Response(serializer.data)

class ClientListIngredientByProducts(APIView):
    """
    Classe para visualizar todos os ingredientes de determinado produto
    """

    def get(self, reuest, pk, product_id):
        products = Product.objects.filter(company=pk).get(pk=product_id)
        ingredients = products.ingredient.all()
        serializer = IngredientSerializer(ingredients, many=True, context={"product_id":product_id})
        return Response(serializer.data)