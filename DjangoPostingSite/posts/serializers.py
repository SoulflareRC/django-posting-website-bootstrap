from django.urls import path,include
from . import views,models
from django_comments.models import Comment
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers,serializers,viewsets
from taggit.serializers import (TagListSerializerField,TaggitSerializer)
from taggit.models import Tag
class PostSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model=models.Post
        fields = '__all__'
class TagSerializer(TaggitSerializer,serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user','user_name','user_email',
                  'comment',
                  'submit_date',
                  'is_public','is_removed']