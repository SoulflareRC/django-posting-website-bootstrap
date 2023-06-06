from django.contrib import admin
from django_comments.models import Comment
from django_comments.admin import CommentsAdmin
from allauth.account.models import EmailAddress
from . import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['post_id']
    list_display = ['title','author','private','pinned','publish_date']
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user']
# class MyCommentsAdmin(CommentsAdmin):
#     list_display = ['name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed']

admin.site.register(models.Post,PostAdmin)
admin.site.register(models.UserInfo,UserInfoAdmin)