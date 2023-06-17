from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from fluent_comments.models import FluentComment
from posts.models import Post,Message,add_owner_permission
class Command(BaseCommand):
    help = "Assign owner permissions for existing "
    def handle(self, *args, **options):
       '''Post'''
       posts = Post.objects.all()
       for post in posts:
            add_owner_permission(post,post.author)
       '''Comment'''
       comments = FluentComment.objects.all()
       for comment in comments:
           add_owner_permission(comment,comment.user)
       '''Message'''
       messages = Message.objects.all()
       for message in messages:
           add_owner_permission(message,message.to_user)

       self.stdout.write(self.style.SUCCESS("Permission assigned successfully!"))
