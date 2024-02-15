from django.contrib import admin

from .models import Product, ProductAttribute, ProductTag, ProductType
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductTag)
admin.site.register(ProductType)
