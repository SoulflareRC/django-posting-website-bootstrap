from django.apps import apps
from django.contrib.auth.models import *
# from .models import Message # can't import directly due to circular import issue




# ---------------Message templates ----------------------------------------------

#----------------Post approval related---------------------
def wait_approval(post):
    '''Send and return a message to the author
    indicating that the post is waiting for approval'''
    print("Creating notification")
    Message = apps.get_model("posts", "Message")
    msg = Message.objects.create(
        from_user = User.objects.get(pk=1),
        to_user = post.author,
        title = f"Your post [{post.title}] is waiting for approval",
        content = f"We've notified staffs to approve your post",
        url = post.get_absolute_url(),
    )
    return msg
def notify_approval(post):
    print("Post approved")
    Message = apps.get_model("posts", "Message")
    msg = Message.objects.create(
        from_user=User.objects.get(pk=1),
        to_user=post.author,
        title=f"Your post [{post.title}] has been approved!",
        content=f"Click here to see your post!",
        url=post.get_absolute_url(),
    )
    return msg
def notify_staff_post(post):
    print("Notifying staffs for approval")
    staffs = User.objects.filter(is_staff=True)
    print("Staffs:",staffs)
    msgs = []
    Message = apps.get_model("posts", "Message")
    for staff in staffs:
        print(staff)
        msg = Message.objects.create(
            from_user=post.author,
            to_user=staff,
            title=f"[{post.title}] by {post.author} is waiting for your approval",
            content=f"Enter the admin site to approve the post",
            url=post.get_absolute_url(),
        )
        msgs.append(msg)
    return msgs
# ------------Post action related---------------------
def notify_pinned(post):
    print("Notifying post pinned")
    Message = apps.get_model("posts", "Message")
    msg = Message.objects.create(
        from_user = User.objects.get(pk=1),
        to_user = post.author,
        title = f"Your post [{post.title}] has been pinned!",
        content = f"Click here to see your post!",
        url = post.get_absolute_url(),
    )
    return msg
# ------------Comment related---------------------
def notify_comment(post,comment):
    '''notify the author that someone has commented their post'''
    print("Creating comment notification")
    Message = apps.get_model("posts", "Message")
    commenter = comment.user
    msg = Message.objects.create(
        from_user = commenter,
        to_user = post.author,
        title = f"{commenter.userinfo.display_name} has commented your post [{post.title}]",
        content = f"{comment.comment}",
        url = post.get_absolute_url(),
    )
    return msg