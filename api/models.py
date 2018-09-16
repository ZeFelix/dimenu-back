from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Owner(User):
    cpf = models.CharField('CPF',max_length=45, unique=True)
    phone = models.CharField('Phone', max_length=45)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


    class Meta:
        verbose_name = "Owner"

class Client(User):
    cpf = models.CharField('CPF', max_length=45, unique=True, blank=True, null=True)
    phone = models.CharField('Phone', max_length=45, unique=True)
    address = models.CharField("Address", max_length=12,blank=True, null=True)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


    class Meta:
        verbose_name = "Client"

class Company(models.Model):
    def company_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/product/id/<filename>
        return 'company/{0}/{1}'.format(instance.id, filename)  

    fantasy_name = models.CharField('Fantasy name', max_length=45, default="company default", unique=True)
    cnpj = models.CharField('CNPJ', max_length=45, unique=True)
    email = models.EmailField('Email', max_length=45, unique=True)
    phone = models.CharField('Phone',max_length=45)
    qrcode_identification = models.CharField("Qr code for identification",max_length=50, unique=True)
    image = models.ImageField("Log of Company", upload_to=company_directory_path, blank=True, null=True)
    owner = models.name = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField("Color of the company", max_length=50, blank=True, null=True, default="#ffffff")
    city  = models.CharField("City",max_length=50, default="Barbalha")
    state = models.CharField("State", max_length=5, default="CE")
    

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.fantasy_name
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["fantasy_name"]

class Employee(User):
    cpf = models.CharField('CPF',max_length=45,unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    
    class Meta:
        verbose_name = "Employee"

class Table(models.Model):
    identification = models.CharField("Table identification",max_length=45)
    qrcode = models.CharField('Qr code for identification of the table',max_length=50, unique=True)
    available = models.BooleanField("Table available",default=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.identification

    class Meta:
        unique_together = ("company","identification")

class Attribute(models.Model):
    
    def attribute_directory_path(instance, filename):
            # file will be uploaded to MEDIA_ROOT/product/id/<filename>
        return 'attribute/{0}/{1}'.format(instance.id, filename)  

    name = models.CharField('Name of the attribute',max_length=45)
    status = models.BooleanField('Status of the attribute',default=True)
    is_additional = models.BooleanField('Indicates if an item is additional')
    image = models.ImageField(upload_to = attribute_directory_path, blank=True, null=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("company","name")
        ordering = ["name"]


class Category(models.Model):

    def category_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/product/id/<filename>
        return 'category/{0}/{1}'.format(instance.id, filename)  
    name = models.CharField('Name',max_length=45)
    color = models.CharField(max_length=45, blank=True, null=True)
    image = models.ImageField("Image of the Category", upload_to=category_directory_path, blank=True, null=True)
    status = models.BooleanField("Status of the category",default=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("company","name")
        ordering = ["name"]

class Ingredient(models.Model):
    
    def ingredient_directory_path(instance, filename):
            # file will be uploaded to MEDIA_ROOT/product/id/<filename>
        return 'ingredient/{0}/{1}'.format(instance.id, filename)   

    name = models.CharField("Ingredient Name", max_length=50)
    is_additional = models.BooleanField("Can is additional?", default=True)
    status = models.BooleanField("Status: available?", default=True)
    image = models.ImageField("Image", upload_to=ingredient_directory_path, blank=True, null=True)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company","name"),)
        ordering = ["name"]

    
class Product(models.Model):
    
    def product_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/product/id/<filename>
        return 'product/{0}/{1}'.format(instance.id, filename)    

    name = models.CharField("Name of the product",max_length=45)
    description = models.TextField('Description of the product')
    price = models.DecimalField("Price of the product",max_digits=6,decimal_places=2)
    status = models.BooleanField('Status of the product',default=True)
    image = models.ImageField(upload_to = product_directory_path, blank=True, null=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    attribute = models.ManyToManyField(Attribute)
    ingredient =models.ManyToManyField(Ingredient, through='ProductIngredient')

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("company","name")
        ordering = ["name"]

class Order(models.Model):
    to_do = models.BooleanField('Order: to do', default=True)
    doing = models.BooleanField('Order: doing',default=False)
    done = models.BooleanField('Order: done', default=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, default=None)

    product = models.ManyToManyField(Product,through='ProductOrder')
    attribute = models.ManyToManyField(Attribute)
    ingredient = models.ManyToManyField(Ingredient, through='IngredientOrder')

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return str(self.id)

class ProductOrder(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True,null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

class ProductIngredient(models.Model):
    grams = models.FloatField("Quantity grams of the produtc.", default=0.0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


class IngredientOrder(models.Model):
    quantity = models.IntegerField(default=1)
    #true: adicionado, false: removido
    is_selected = models.BooleanField('Is selected?',default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


class Avaliation(models.Model):
    note = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


    def __str__(self):
        return "User - {}, Note: {}; Produto: {}".format(self.client.username, self.note, self.product)
