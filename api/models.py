from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Owner(User):
    cpf = models.CharField('CPF',max_length=12, unique=True)
    phone = models.CharField('Phone', max_length=15)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


    class Meta:
        verbose_name = "Owner"

class Client(User):
    cpf = models.CharField('CPF', max_length=12, unique=True)
    phone = models.CharField('Phone', max_length=12, unique=True)
    address = models.CharField("Address", max_length=12,blank=True, null=True)

    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)


    class Meta:
        verbose_name = "Client"

class Company(models.Model):
    fantasy_name = models.CharField('Fantasy name', max_length=45, default="company default")
    cnpj = models.CharField('CNPJ', max_length=45, unique=True)
    email = models.EmailField('Email', max_length=45, unique=True)
    phone = models.CharField('Phone',max_length=13)
    qrcode_identification = models.CharField("Qr code for identification",max_length=50, unique=True)
    owner = models.name = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.fantasy_name
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["fantasy_name"]

class Employee(User):
    cpf = models.CharField('CPF',max_length=25,unique=True)
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
    name = models.CharField('Name',max_length=45)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("company","name")
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, default=None)

    product = models.ManyToManyField(Product,through='ProductOrder')
    attribute = models.ManyToManyField(Attribute,through='OrderAttribute')

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


class OrderAttribute(models.Model):
    quantity = models.IntegerField(default=1)
    #true: adicionado, false: removido
    status = models.BooleanField('Indicates whether the attribute was removed and added to this order',default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

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
        return "Avaliation of the user - " + self.user.username