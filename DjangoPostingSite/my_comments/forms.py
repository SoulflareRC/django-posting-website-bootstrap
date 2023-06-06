
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
from fluent_comments.forms import DefaultCommentForm
from crispy_forms.layout import Column, Layout, Row
from django.utils.functional import cached_property

from fluent_comments import appsettings
from fluent_comments.forms.base import AbstractCommentForm, PreviewButton, SubmitButton
from fluent_comments.forms.helper import CompactLabelsCommentFormHelper

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
    def  clean(self):
        cleaned_data =super(CommentFormOnlyContent, self).clean()
        cleaned_data.pop('preview',None)
        return cleaned_data
class ModifiedCommentForm(CompactLabelsCommentForm):
    name = forms.CharField(label=pgettext_lazy("Person name", "Name"), max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField(label=_("Email address"), widget=forms.HiddenInput)
    url = forms.URLField(label=_("URL"), required=False, widget=forms.HiddenInput)
    comment = forms.CharField(label=_('Comment'),
                              widget=forms.Textarea(attrs={"placeholder": 'Write something friendly...'}),
                              max_length=1000)

    @cached_property
    def helper(self):
        # Initialize on demand
        helper = CompactLabelsCommentFormHelper()
        helper.layout = Layout(*self.fields.keys())
        helper.add_input(SubmitButton())
        # helper.add_input(PreviewButton()) # disable preview, this causes bug
        return helper