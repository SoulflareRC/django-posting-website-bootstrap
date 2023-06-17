from django.shortcuts import render,reverse,get_object_or_404,redirect
'''Views'''
from guardian.mixins import PermissionRequiredMixin,LoginRequiredMixin
# from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.http import *
'''Models '''
from django.contrib import messages
from posts import models

'''Forms'''
from posts import forms

from .generics import StaffRequiredMixin,RedirectActionView

class PostView(generic.DetailView):
    template_name = "posts/post.html"
    model = models.Post
    context_object_name = "post"

    def get(self, request: HttpRequest, *args, **kwargs):
        print("Request user:",request.user,request.user.pk )
        # delete if parameter specifies delete=True
        post = self.get_object()
        # redirect to index if this post is private
        if post.private and post.author != request.user:
            return redirect(reverse("posts:index"))
        '''
        Normal query actions. 

        '''
        c = request.GET.get('c', None)
        if c:
            return redirect(reverse('posts:post', kwargs={'pk': self.kwargs['pk']}) + f'#c{c}')  # Locate the comment
        '''Show messages'''
        if not post.approved:
            messages.add_message(request,messages.INFO,"Your post is waiting for approval")

        return super(PostView, self).get(request, *args, **kwargs)
class PostCreateView(LoginRequiredMixin,generic.edit.CreateView):
    template_name = "posts/editor.html"
    form_class = forms.PostForm
    model = models.Post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)
    def get_success_url(self):
        return self.object.get_absolute_url()
    def get(self, request, *args, **kwargs):
        print(request.user)
        return super(PostCreateView, self).get(request, *args, **kwargs)
class PostEditView(PermissionRequiredMixin, LoginRequiredMixin,generic.edit.UpdateView):
    permission_required = "change_post"
    raise_exception = True
    template_name = "posts/editor.html"
    form_class = forms.PostForm
    model = models.Post
    def get_success_url(self):
        return self.object.get_absolute_url()
class PostDeleteView(RedirectActionView):
    permission_required = "delete_post"
    model = models.Post
    def get_url(self):
        return reverse('posts:index')
    def actions(self):
        obj = self.get_object()
        obj.delete()
class PostSaveToggleView(RedirectActionView):
    permission_required = [] # no permission needed, only login required
    model = models.Post
    def actions(self):
        obj = self.get_object()
        user = self.request.user
        if user in obj.saved_by.all():
            print(f"User {user} unsaved post {obj}")
            obj.saved_by.remove(user)
        else:
            print(f"User {user} saved post {obj}")
            obj.saved_by.add(user)
        obj.save()
class PostPrivateToggleView(RedirectActionView):
    permission_required = "change_post"
    model = models.Post
    def actions(self):
        obj = self.get_object()
        if obj.private:
            obj.private = False
        else:
            obj.private = True
        obj.save()
class PostPinnedToggleView(StaffRequiredMixin,RedirectActionView):
    permission_required = []
    model = models.Post
    def actions(self):
        obj = self.get_object()
        if obj.pinned:
            obj.pinned = False
        else:
            obj.pinned = True
        obj.save()