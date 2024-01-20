from django.shortcuts import render
from django.shortcuts import render
from .serializers import BlogTopicSerializer, PostTypeSerializer, TagSerializer, BlogPostSerializer, BlogPostPreviewSerializer
from .models import BlogTopic, PostType, Tag, BlogPost
from rest_framework import viewsets, generics, status, filters
from .manager import Assistant
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from rest_framework.response import Response


# Create your views here.
class BlogTopicViewSet(viewsets.ModelViewSet):
    queryset = BlogTopic.objects.all()
    serializer_class = BlogTopicSerializer
    
class PostTypeViewSet(viewsets.ModelViewSet):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    
class BlogPostPreviewViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostPreviewSerializer
    
    
@api_view(['GET'])
def write_posts(request):
    assistant = Assistant()
    assistant.write_all()
    return Response(status=status.HTTP_200_OK)