from django.contrib import admin
from django_comments.models import Comment
from django_comments.admin import CommentsAdmin
from allauth.account.models import EmailAddress
from . import models
# Register your models here.
@admin.action(description="Approve selected posts")
def approve_posts(modeladmin,request,queryset):
    queryset.update(approved=True)

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['post_id']
    list_display = ['title','author','approved','private','pinned','publish_date']
    list_filter = ["approved","private","pinned","author"]
    actions = [approve_posts]
class MessageAdmin(admin.ModelAdmin):
    list_display = ["from_user","to_user", 'title',"sent_date","read"]
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user','display_name']
class SiteInfoAdmin(admin.ModelAdmin):
    pass
# class MyCommentsAdmin(CommentsAdmin):
#     list_display = ['name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed']

admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Message,MessageAdmin)
admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.SiteInfo,SiteInfoAdmin)