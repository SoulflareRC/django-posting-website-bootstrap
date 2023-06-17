from django.views import generic
from posts import models
from django.http import HttpResponseForbidden
from django.shortcuts import reverse
from django.contrib.auth.models import User

class ProfileUpdateView(generic.UpdateView):
    '''Update userinfo of user'''
    # a bit tricky, since it needs to convert back and forth between userinfo and user.
    template_name = 'posts/profile_update.html'
    model = models.UserInfo
    context_object_name = 'profile'
    fields = ['icon','profile_bg','display_name','slogan','github_link','linkedin_link']
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.userinfo.pk!=self.kwargs['pk']:
            '''only allow this user'''
            return HttpResponseForbidden()
        else:
            return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
    def get_success_url(self):
        user = self.get_object().user
        return reverse('posts:user', kwargs={'pk': user.pk})
class ProfileView(generic.DetailView):
    template_name = "posts/profile.html"
    model = User # more intuitive to use User instead of UserInfo
    context_object_name = 'profile' # this should not be 'user', to avoid conflict with request.user
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        '''prevent exposing private posts by adding this.'''
        if self.request.user.is_authenticated:
            posts = models.Post.objects.visible_to_user(user)
        else:
            posts = models.Post.objects.visible_to_user(-1)
        posts = posts.filter(author=self.get_object())
        context['profile_posts'] = posts
        return context