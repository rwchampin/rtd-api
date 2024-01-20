from django.db import models
from django.utils.text import slugify


import readtime
# Create your models here.
class BlogTopic(models.Model):
    url = models.URLField(max_length=200, unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.url
    
class PostType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post_type = models.ForeignKey(PostType, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    keywords = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    read_time = models.CharField(max_length=50, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.read_time = str(readtime.of_html(self.content))
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title