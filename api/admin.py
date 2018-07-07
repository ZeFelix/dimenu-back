from django.contrib import admin
from .models import *

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username','is_client')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Table)
admin.site.register(Attribute)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(OrderAttribute)
admin.site.register(Avaliation)