
from django import forms
from django_comments.forms import CommentForm,CommentDetailsForm,CommentSecurityForm,get_model
from .models import CommentWithTitle
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms.utils import ErrorDict
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.encoding import force_str
from django.utils.text import get_text_list
from django.utils import timezone
from django.utils.translation import pgettext_lazy, ngettext, gettext, gettext_lazy as _
from fluent_comments.forms.compact import CompactLabelsCommentForm
# class CommentFormWithTitle(CommentForm):
#     title = forms.CharField(max_length=300)
#
#     def get_comment_create_data(self, **kwargs):
#         # Use the data of the superclass, and add in the title field
#         data = super().get_comment_create_data(**kwargs)
#         data['title'] = self.cleaned_data['title']
#         return data
class CompactCommentFormOnlyContent(CompactLabelsCommentForm):
    name = forms.CharField(label=pgettext_lazy("Person name", "Name"), max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField(label=_("Email address"), widget=forms.HiddenInput)
    url = forms.URLField(label=_("URL"), required=False, widget=forms.HiddenInput)
    comment = forms.CharField(label=_('Comment'), widget=forms.Textarea(attrs={"placeholder":'Write something friendly...'}),
                              max_length=1000)
class CommentFormOnlyContent(CommentDetailsForm):
    name = forms.CharField(label=pgettext_lazy("Person name", "Name"), max_length=50,widget=forms.HiddenInput)
    email = forms.EmailField(label=_("Email address"),widget=forms.HiddenInput)
    url = forms.URLField(label=_("URL"), required=False,widget=forms.HiddenInput)
    comment = forms.CharField(label=_('Comment'), widget=forms.Textarea(attrs={"placeholder":'Write something friendly...'}),
                              max_length=1000)
    # as along as name,email are hidden...they will be filled with user's name/email if the user is authenticated