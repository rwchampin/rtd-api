from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'blog-topics', views.BlogTopicViewSet)
router.register(r'post-types', views.PostTypeViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'blog-posts', views.BlogPostViewSet)

urlpatterns = [
    path('write-posts/', views.write_posts),
    path('', include(router.urls)),

]
