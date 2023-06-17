'''DRF'''
from django_comments.models import Comment
from posts import models,serializers
from rest_framework import filters,viewsets
from taggit.models import Tag
from rest_framework.request import Request
'''DRF API views'''
class PostsAPIView(viewsets.ModelViewSet):
    search_fields = ['title','content','author__username']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    # filter_backends = [DjangoFilterBackend]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    def get_queryset(self):
        '''Hide private posts'''
        queryset = super(PostsAPIView, self).get_queryset()
        return queryset.filter(private=False)
class CommentsAPIView(viewsets.ModelViewSet):
    search_fields = ['comment','user_email','user_name']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
class TagsAPIView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer