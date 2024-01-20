from rest_framework import serializers
 
from .models import BlogTopic, PostType, Tag, BlogPost

class BlogTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTopic
        fields = ['url', 'used']
        
class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = ['name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        level = 2
        fields = ['title', 'subtitle', 'content', 'slug', 'created', 'updated', 'topic', 'post_type', 'tags']
        

class BlogPostPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        level = 2
        fields = ['title', 'subtitle', 'slug', 'created', 'updated', 'topic', 'post_type', 'tags']