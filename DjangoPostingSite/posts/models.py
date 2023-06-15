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
from .message_utils import *
# from . import message_templates

def default_image_folder():
    return str(settings.DEFAULT_IMAGE_FOLDER)

class PostManager(models.Manager):

    def visible_to_user(self,user):
        '''A user can view:
            1. Posts posted by self
            2. public posts
        '''
        queryset = self.get_queryset()
        queryset = queryset.filter(author=user)
        return queryset | self.public()
    def approved(self):
        queryset = self.get_queryset()
        return queryset.filter(approved=True)
    def public(self):
        queryset = self.approved()
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

    approved = models.BooleanField(default=False) # defaulted to false so that staffs can approve the posts.


    objects = PostManager()
    class Meta:
        ordering = ["-pinned","-publish_date","title"]
        permissions = (
            # default permissions:add,change,delete,view
            # ('view_post'), # default view
            # ('create_post'), # default add
            # ('delete_post'), # default delete
            # ('edit_post'),   # default change
            ('approve_post',"Approve post"),
            ('pin_post',"Pin post"),
            ('private_post','Set post as private'),
            # ('save_post')
        )
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("posts:post", kwargs={'pk':self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None
  ):
        '''Send 2 messages:
            1. Admin->author: your post is waiting for approval
            2. Author->All staffs: please approve this post
         '''

        if self.pk is None:
            print("Post created")
            post = super(Post, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
            add_owner_permission(self, self.author)
            wait_approval(self)
            notify_staff_post(self)
        else:
            print("Post updated")

            post = super(Post, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return post
@receiver(pre_save,sender=Post)
def approve_update_signal(sender,instance,**kwargs):
    '''Notify author that their post is approved when approved updated'''
    if instance.pk and Post.objects.filter(pk=instance.pk).exists():
        print("Approve update")
        prev_instance = Post.objects.get(pk=instance.pk)
        if prev_instance.approved != instance.approved and instance.approved:
            notify_approval(instance)
from fluent_comments.models import FluentComment
@receiver(post_save,sender=FluentComment)
def notify_comment_signal(sender,instance,created,**kwargs):
    if created:
        print("Comment was created")
        '''Comment was created'''
        post = instance.content_object
        comment = instance
        if comment.user != post.author:
            notify_comment(post,comment)


class Message(models.Model):
    from_user = models.ForeignKey(User, null=False, blank=False,
                                  default=0,
                                  on_delete=models.CASCADE,
                                  related_name="msg_sent")  # maybe this can be null, so it becomes an announcement?
    to_user = models.ForeignKey(User, null=False, blank=False,
                                default=0,
                                on_delete=models.CASCADE, related_name="msg_recv")
    title = models.CharField(max_length=50,blank=False,null=False)
    # content = MartorField()
    content = models.TextField(null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    read = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-sent_date","from_user"]
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

# ----Permission utils --------
# # default permissions:add,change,delete,view
# other permissions: pin, approve
from guardian.shortcuts import assign_perm

def add_owner_permission(obj:Post,user):
    # assign the owner of the object change,delete,view permissions
    # assign_perm(f'change_{obj}',)
    print(f"Adding owner permissions to {user} for {obj}")
    model_name = obj._meta.model_name
    print("Table name:", model_name)
    assign_perm(f'change_{model_name}',user,obj)
    assign_perm(f'delete_{model_name}', user, obj)
    assign_perm(f'view_{model_name}', user, obj)

