from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import uuid
from django.conf import settings
from pathlib import Path,WindowsPath
from martor.models import MartorField
from django.contrib.auth.models import *
from taggit.managers import TaggableManager
from django_comments.models import Comment
from django_comments.templatetags.comments import *
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
from django.shortcuts import reverse

def default_image_folder():
    return str(settings.DEFAULT_IMAGE_FOLDER)

class PostManager(models.Manager):
    def visible_to_user(self,user):
        queryset = self.get_queryset()
        private_posts = queryset.filter(private=True)
        private_posts = private_posts.exclude(author=user)
        queryset = queryset.exclude(id__in=private_posts)
        return queryset
    def public(self):
        queryset = self.get_queryset()
        return queryset.filter(private=False)
class Post(models.Model):
    post_id = models.UUIDField(default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    # cover_default_dir = Path(settings.MEDIA_ROOT / 'covers' / 'defaults')
    cover = models.ImageField(blank=False,null=False,
                              upload_to= settings.MEDIA_ROOT / 'covers',
                              default= default_image_folder()+"/post_cover_default.png"
                              )
    content = MartorField()
    publish_date = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    saved_by = models.ManyToManyField(User,related_name="saved_posts",blank=True) # this has to have a diff related name or user.post_set is ambiguous
    private = models.BooleanField(default=False,blank=False,null=False)
    pinned = models.BooleanField(default=False,blank=False,null=False)
    comments = GenericRelation(Comment,object_id_field='object_pk')

    objects = PostManager()
    class Meta:
        ordering = ["-pinned","-publish_date","title"]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("posts:post", kwargs={'pk':self.pk})


# catch signal and create a profile for each user when user created.
@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance,display_name=instance.username)
class UserInfo(models.Model):
    # to extend the predefined user model, use one2one field
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50,blank=False,null=False,default="None")
    slogan = models.CharField(max_length=200,blank=True)
    icon = models.ImageField(max_length=500, blank=True,
                             upload_to=settings.MEDIA_ROOT / 'user' / 'icon',
                             default='icon_default.png')
    profile_bg = models.ImageField(max_length=500, blank=True,
                                   upload_to=settings.MEDIA_ROOT / 'user' / 'profile_background',
                                   default=default_image_folder()+"/profile_bg_default.png")

    linked_link = models.URLField(blank=True,null=True)
    github_link = models.URLField(blank=True,null=True)


class SiteInfo(models.Model):
    site_icon = models.ImageField(max_length=500, blank=True,
                                  upload_to=settings.MEDIA_ROOT / 'global' / 'site_icon',
                                  default= default_image_folder()+"/site_icon_default.png" )
    site_title = models.CharField(max_length=50, blank=True, default="Site")
    site_contact_bg = models.ImageField(max_length=500,  blank=True,
                                        upload_to=settings.MEDIA_ROOT / 'global' / 'site_contact' / 'bg',
                                        default=default_image_folder()+"/site_contact_bg_default.png" )
    owner = models.ForeignKey(User,on_delete=models.CASCADE)


# # assign group(and permission) to staff when a user becomes a staff
# @receiver(post_save,sender=User)
# def add_user_to_group(sender, instance, created, **kwargs):
#     if not created:
#         group = Group.objects.get(name='staffs')  # Replace with the actual group name
#         if instance.is_staff and not group.user_set.filter(pk=instance.pk).exists():
#             # User is staff and not in the group, so add them to the group
#             instance.groups.add(group)
#         elif not instance.is_staff and group.user_set.filter(pk=instance.pk).exists():
#             # User is not staff but in the group, so remove them from the group
#             instance.groups.remove(group)