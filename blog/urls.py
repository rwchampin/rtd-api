from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'blog-topics', views.BlogTopicViewSet)
router.register(r'post-types', views.PostTypeViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'blog-posts', views.BlogPostViewSet)
router.register(r'blog-posts-preview', views.BlogPostPreviewViewSet)
router.register(r'blog-posts-by-tag/(?P<slug>[-\w]+)', views.BlogPostByTagViewSet, basename='blogpost-by-tag')
router.register(r'blog-posts-by-post-type/(?P<slug>[-\w]+)', views.BlogPostByPostTypeViewSet, basename='blogpost-by-post-type')


urlpatterns = [
    path('write-posts/', views.write_posts),
    path('', include(router.urls)),

]
