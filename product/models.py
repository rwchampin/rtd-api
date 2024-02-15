from django.db import models

# Create your models here.
from django.db import models

class ProductTag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    
class ProductType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    hosted_url = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    patreon_url = models.URLField(null=True, blank=True)

    
    
    def get_tags(self):
        return ProductTag.objects.filter(product=self)
    
    def get_attributes(self):
        return ProductAttribute.objects.filter(product=self)
    
    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product} - {self.name}: {self.value}"
 