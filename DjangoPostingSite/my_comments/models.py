from django.db import models
from django_comments.abstracts import CommentAbstractModel,BaseCommentAbstractModel
# using CommentAbstractModel will add field to existing fields of the form
# class CommentWithTitle(CommentAbstractModel):
#     title = models.CharField(max_length=300)
class CommentContentOnly(BaseCommentAbstractModel ):
    content = models.CharField(max_length=1000)
