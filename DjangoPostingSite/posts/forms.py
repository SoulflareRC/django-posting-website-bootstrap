from fluent_comments.forms.base import *
from django.contrib.auth.forms import *
from . import models

class PostForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PostForm, self).__init__(*args,**kwargs)
        '''convenient way to tagify taggit fields'''
        self.fields['tags'].widget.attrs.update({
            "class":"tagify",
            "placeholder":"Add tags for post"
        })

    class Meta:
        model = models.Post
        fields = ["title","content","tags","cover"]
        labels = {"title":"Title","desc":"Description"}

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        # fields = '__all__' # fields or excludes must be specified
        exclude = ['user']