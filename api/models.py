from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
    fantasy_name = models.CharField('Fantasy name', max_length=45, default="company default")
    cnpj = models.CharField('CNPJ', max_length=45, unique=True)
    email = models.EmailField('Email', max_length=45, unique=True)
    phone = models.CharField('Phone',max_length=13)
    qrcode_identification = models.CharField("Qr code for identification",max_length=50, unique=True)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.fantasy_name
    
    class Meta:
        verbose_name_plural = "Companies"

class CustomUser(User):
    cpf = models.CharField('CPF',max_length=12)
    phone = models.CharField('Phone', max_length=15)
    is_client = models.BooleanField('Is mobile',default=False)
    is_owner = models.BooleanField('Is owner',default=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        unique_together = (("company","cpf"),("is_client","cpf"))

class Table(models.Model):
    identification = models.CharField("Table identification",max_length=45)
    qrcode = models.CharField('Qr code for identification of the table',max_length=50, unique=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.identification

    class Meta:
        unique_together = ("company","identification")

class Attribute(models.Model):
    name = models.CharField('Name of the attribute',max_length=45)
    status = models.BooleanField('Status of the attribute')
    is_additional = models.BooleanField('Indicates if an item is additional')
    image = models.ImageField(upload_to='attributes/%Y/%m/%d', blank=True, null=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("company","name")


class Category(models.Model):
    name = models.CharField('Name',max_length=45)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("company","name")

class Product(models.Model):
    name = models.CharField("Name of the product",max_length=45)
    description = models.TextField('Description of the product')
    price = models.DecimalField("Price of the product",max_digits=6,decimal_places=2)
    status = models.BooleanField('Status of the product')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    product_attribute = models.ManyToManyField(Attribute)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("company","name")

class Order(models.Model):
    to_do = models.BooleanField('Order: to do', default=True)
    doing = models.BooleanField('Order: doing',default=False)
    done = models.BooleanField('Order: done', default=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    product = models.ManyToManyField(Product,through='ProductOrder')
    attribute = models.ManyToManyField(Attribute,through='OrderAttribute')

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.id

class ProductOrder(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class OrderAttribute(models.Model):
    quantity = models.IntegerField(default=1)
    #true: removido, false: adicionado
    status = models.BooleanField('Indicates whether the attribute was removed and added to this order')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

class Avaliation(models.Model):
    note = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  