from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import *
from django.contrib.auth.models import Permission, Group, User

# realiza as relações de muitos relacionamentos
from drf_writable_nested import WritableNestedModelSerializer

class Base64ImageField(serializers.ImageField):
    """
    Classe para converter imagem base 64 enviado ao servidor
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

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
    image = Base64ImageField(max_length = None,use_url = True, required = False, allow_null = True)    
    class Meta:
        model = Company
        fields = ('id', 'fantasy_name', 'cnpj', 'email', 'phone', 'qrcode_identification','color','city','state','image','owner')
        extra_fields = {
            "color" : {"required":False}
        }

class ProductIngredientSerializer(serializers.ModelSerializer):
    product_ingredient_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = ProductIngredient
        fields = ['product_ingredient_id','grams','ingredient']


class IngredientOrderSerializer(serializers.ModelSerializer):
    ingredient_order_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = IngredientOrder
        fields = ['ingredient_order_id','quantity','is_selected','ingredient']


class IngredientSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length = None,use_url = True, required = False, allow_null = True)

    class Meta:
        model = Ingredient
        fields = ('id','name','is_additional',"status","image","company")
        extra_fields = {
            "image":{"required":False}
        }
    
    def to_representation(self, instance):
        """
        Método para atribuir na representação do ingredient as gramas daquele ingrediente em determinado produto,
        caso exista grama,
        o id do produto é passado pela variável context da view
        """
        representation = super().to_representation(instance)
        product_id = self.context.get("product_id")
        try:
            product_ingredient = ProductIngredient.objects.filter(ingredient=instance.id, product=product_id).first()
            representation["grams"] = product_ingredient.grams
        except Exception as e:
            pass

        return  representation
        

class CategorySerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length = None,use_url = True, required = False, allow_null = True)
    class Meta:
        model = Category
        fields = ['id','name', 'color','image','company',"status"]


class AttributeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length = None,use_url = True, required = False, allow_null = True)

    class Meta:
        model = Attribute
        fields = ['id','name','status','is_additional','image','company']

class ProductSerializer(WritableNestedModelSerializer):
    image = Base64ImageField(max_length = None,use_url = True, required = False, allow_null = True)
    attribute = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Attribute.objects.all())
    ingredient = ProductIngredientSerializer(source='productingredient_set',many=True)

    class Meta:
        model = Product
        fields = ["id","name", "description", "price", "status", "image", "company", "category","attribute","ingredient"]
        extra_fields = {
            "ingredient":{"required":False}
        }

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id','identification', 'qrcode','available', 'company']

class AvaliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliation
        fields = ['id','note', 'client', 'product', 'company']


class ProductOrderSerializer(serializers.ModelSerializer):
    product_order_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = ProductOrder
        fields = ['product_order_id','quantity','product']

class OrderSerializer(WritableNestedModelSerializer):
    product = ProductOrderSerializer(source='productorder_set',many=True)
    attribute = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Attribute.objects.all())
    client = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Client.objects.all())
    employee = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Employee.objects.all())
    ingredient = IngredientOrderSerializer(source='ingredientorder_set', many=True)

    class Meta:
        model = Order
        fields = ['id','to_do','doing','done','client','employee','company','table','product','attribute','ingredient']


class OwnerSerializer(serializers.ModelSerializer): 
    user_permissions = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Permission.objects.all()) 
    groups = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Group.objects.all()) 
 
    password = serializers.CharField(write_only = True) 
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())]) 
 
    class Meta: 
        model = Owner 
        fields = ['id','password','username','first_name',"last_name",'email','cpf','phone','is_staff','user_permissions','groups']  

class ClientSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Permission.objects.all()) 
    groups = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Group.objects.all()) 
    
    password = serializers.CharField(write_only = True) 
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)
    
    class Meta:
        model = Client
        fields = ['id','password','username','first_name',"last_name",'email','cpf','phone','address','is_staff','user_permissions','groups']  
        extra_kwargs = {
            "cpf": {"required":False},
            "address": {"required":False},
            "last_name": {"required":False}
        }


class EmployeeSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Permission.objects.all()) 
    groups = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Group.objects.all()) 

    password = serializers.CharField(write_only = True) 
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)

    company = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Company.objects.all())

    class Meta:
        model = Employee
        fields = ['id','password','username','first_name',"last_name",'email','cpf','company','is_staff','user_permissions','groups']  