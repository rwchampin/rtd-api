from django.contrib import admin
from .models import BlogTopic, PostType, Tag, BlogPost
# Register your models here.
admin.site.register(BlogTopic)
admin.site.register(PostType)
admin.site.register(Tag)
admin.site.register(BlogPost)
