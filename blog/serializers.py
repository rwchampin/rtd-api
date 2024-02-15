from rest_framework import serializers
 
from .models import BlogTopic, PostType, Tag, BlogPost, Comment


# mixin for pretty date
class PrettyDateMixin(object):
    def get_updated_pretty(self, obj):
        # format date to 9-10-2020
        return obj.updated.strftime("%b %d, %Y")
    
    def get_created_pretty(self, obj):
        return obj.created.strftime("%b %d, %Y")
    
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

class BlogPostSerializer(serializers.ModelSerializer, PrettyDateMixin):
    # created formatted date with mixin
    updated_pretty = serializers.SerializerMethodField()
    class Meta:
        model = BlogPost
        depth = 2
        fields = ['title', 'subtitle', 'content', 'slug', 'created', 'updated', 'updated_pretty', 'read_time', 'post_type', 'tags', 'keywords', 'description']
        

class BlogPostPreviewSerializer(serializers.ModelSerializer, PrettyDateMixin):
    # created formatted date
    updated_pretty = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        depth = 2
        fields = ['title', 'subtitle', 'slug', 'updated_pretty', 'updated', 'read_time', 'post_type', 'tags', 'description']
        
        

# class CommentSerializer(serializers.ModelSerializer):
#     replies = serializers.SerializerMethodField()

#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'post', 'parent', 'content', 'created_at', 'updated_at', 'replies']

#     def get_replies(self, obj):
#         if obj.is_reply:
#             return None  # No further nesting for replies
#         replies = obj.replies.all()
#         return CommentSerializer(replies, many=True).data