from django.contrib import admin
from .models import *

# Register your models here.

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 1

class AttributeOrderInline(admin.TabularInline):
    model = OrderAttribute
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = (ProductOrderInline,AttributeOrderInline,) 

admin.site.register(Company)
admin.site.register(Table)
admin.site.register(Attribute)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Avaliation)