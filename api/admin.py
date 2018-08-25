from django.contrib import admin
from .models import *

# Register your models here.

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 1


admin.site.register(Company)
admin.site.register(Table)
admin.site.register(Attribute)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Avaliation)
admin.site.register(Owner)
admin.site.register(Client)
admin.site.register(Employee)