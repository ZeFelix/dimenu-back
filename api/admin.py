from django.contrib import admin
from .models import *

# Register your models here.

class ProductOrderInline(admin.TabularInline): 
    model = ProductOrder 
    extra = 1 
class IngredientOrderInline(admin.TabularInline):  
    model = IngredientOrder 
    extra = 1  
 
class ProductIngredient(admin.TabularInline): 
    model = ProductIngredient 
    extra = 1 
  
class OrderAdmin(admin.ModelAdmin):  
    inlines = (ProductOrderInline,IngredientOrderInline,)  
 
class ProductAdmin(admin.ModelAdmin): 
    inlines = (ProductIngredient,) 
         
 
class AvaliationAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'note', 'company')
    list_filter = ('company', 'product', 'client')

admin.site.register(Company) 
admin.site.register(Table) 
admin.site.register(Attribute) 
admin.site.register(Category) 
admin.site.register(Product, ProductAdmin) 
admin.site.register(Order, OrderAdmin) 
admin.site.register(Ingredient) 
admin.site.register(Avaliation, AvaliationAdmin) 
admin.site.register(Owner) 
admin.site.register(Client) 