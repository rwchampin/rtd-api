from django.shortcuts import render, get_object_or_404
from .serializers import BlogTopicSerializer, PostTypeSerializer, TagSerializer, BlogPostSerializer, BlogPostPreviewSerializer
from .models import BlogTopic, PostType, Tag, BlogPost
from rest_framework import viewsets, generics, status, filters,pagination
from .manager import Assistant
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from rest_framework.response import Response


class BlogPostPreviewPagination(pagination.PageNumberPagination):
    page_size = 9  # the no. of company objects you want to send in one go

# Create your views here.
class BlogTopicViewSet(viewsets.ModelViewSet):
    queryset = BlogTopic.objects.all()
    serializer_class = BlogTopicSerializer
    
class PostTypeViewSet(viewsets.ModelViewSet):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer
    lookup_field = 'slug'
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    
class BlogPostPreviewViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostPreviewSerializer
    pagination_class = BlogPostPreviewPagination
    lookup_field = 'slug'
    

class BlogPostByTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPreviewPagination

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=tag_slug)
        return BlogPost.objects.filter(tags=tag)

class BlogPostByPostTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPostSerializer
    pagination_class = BlogPostPreviewPagination

    def get_queryset(self):
        post_type_slug = self.kwargs['slug']
        post_type = get_object_or_404(PostType, slug=post_type_slug)
        return BlogPost.objects.filter(post_type=post_type)

@api_view(['GET'])
def write_posts(request):
    assistant = Assistant()
    assistant.write_all()
    return Response(status=status.HTTP_200_OK)