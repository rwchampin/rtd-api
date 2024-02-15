from django.db import models
from django.utils.text import slugify
from django.conf import settings
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
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    
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
    # author = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_likes', blank=True)

    def save(self, *args, **kwargs):
        self.read_time = str(readtime.of_html(self.content))
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updated']
        

class Comment(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True)

    # def __str__(self):
    #     return f"Comment by {self.user.username} on {self.post}"

    @property
    def is_reply(self):
        return self.parent is not None

    class Meta:
        ordering = ['-created_at']  # Orders comments by the most recent
        