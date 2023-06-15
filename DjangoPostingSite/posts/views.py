from django.shortcuts import render,reverse,get_object_or_404,redirect
'''Views'''
from guardian.mixins import PermissionRequiredMixin,LoginRequiredMixin
# from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.http import *

'''Models '''
from django.db.models import Count,Sum,Q,Case,When,F,BooleanField,Value
from django.contrib.auth.models import *
from django_comments.models import Comment
from django.contrib import messages
from taggit.models import Tag
from . import models

'''Forms'''
from . import forms

'''Decorators'''
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required

'''DRF'''
from . import models,serializers
from rest_framework import filters,viewsets
from rest_framework.request import Request

class TagsView(generic.TemplateView):
    template_name = "posts/tags_page.html"

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
class PostDeleteView(PermissionRequiredMixin,LoginRequiredMixin, generic.RedirectView,generic.detail.SingleObjectMixin):
    permission_required = "delete_post"
    raise_exception = True
    model = models.Post
    def get_redirect_url(self, *args, **kwargs):
        obj = self.get_object()
        print("Deleted post ",obj)
        obj.delete()
        return reverse("posts:index")

# class EditorView(generic.FormView
#                 ,LoginRequiredMixin
#                  ):
#     '''Create & Update post'''
#     template_name = "posts/editor.html"
#     form_class = forms.PostForm
#     def post(self, request:HttpRequest, *args, **kwargs):
#         query_post = request.GET.get('post', None)
#         # usage: /posts/editor?post=<pk>
#         f = self.form_class(request.POST, request.FILES)
#         if query_post: # update post
#             query_post = int(query_post)
#             post = get_object_or_404(models.Post, pk=query_post)
#             if post.author==request.user:
#                 f = self.form_class(request.POST,request.FILES,instance=post)
#             else:
#                 return HttpResponseForbidden("You are not allowed to edit this post.")
#         if f.is_valid():# hmm a form must be validated to be saved
#             new_form = f.save(commit=False)
#             new_form.author = request.user
#             f.save()
#
#             return redirect(reverse('posts:post', kwargs={'pk': new_form.pk}))
#         return self.get(request,*args,**kwargs)
#
#     def get(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect(reverse("posts:index"))
#         query_post = request.GET.get('post',None)
#         #usage: /posts/editor?post=<pk>
#         print(query_post)
#         if query_post:
#             query_post = int(query_post)
#             post = get_object_or_404(models.Post,pk=query_post)
#             if request.user != post.author:
#                 # return redirect(reverse("posts:post",kwargs={'pk':query_post}))
#                 return redirect(reverse("posts:post",kwargs={'pk':query_post}))
#             print(post.content)
#             form = forms.PostForm(instance=post)
#             context = self.get_context_data(**kwargs)
#             context['form'] = form
#             return render(request,self.template_name,context=context)
#         print("Nothing happens")
#         return super(EditorView, self).get(request, *args, **kwargs)
class ProfileUpdateView(generic.UpdateView):
    '''Update userinfo of user'''
    # a bit tricky, since it needs to convert back and forth between userinfo and user.
    template_name = 'posts/profile_update.html'
    model = models.UserInfo
    context_object_name = 'profile'
    fields = ['icon','profile_bg','display_name','slogan']

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
class InboxView(generic.DetailView):
    template_name = "posts/inbox.html"
    model = User
    context_object_name = 'profile'
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super(InboxView, self).get_context_data(**kwargs)
        user_msgs = models.Message.objects\
            .filter(Q(to_user=user)|Q(from_user=user))
        user_new_msgs = user_msgs.filter(to_user=user).filter(read=False)
        unread_msg_ids = list(user_new_msgs.values_list('id',flat=True))
        print(unread_msg_ids)
        user_new_msgs.update(read=True)

        messages.add_message(self.request, messages.INFO, f"You have {len(unread_msg_ids)} unread messages")
        context["user_msgs"] = user_msgs
        context["unread_msg_ids"] = unread_msg_ids
        return context
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
        Post actions(one-click): 
        save,delete 
        '''
        '''
        "My post-only" actions. 
        delete, set private
        '''
        if request.user.is_authenticated and request.user == post.author:
            '''delete '''
            delete = request.GET.get('delete', None)
            if delete == 'True':
                # authenticated, delete the post
                # hard delete all the comments associated with this post when post is hard deleted.
                associated_comments = post.comments.all()
                associated_comments.delete()
                post.delete()
                return redirect(reverse("posts:index"))
            '''set private'''
            private = request.GET.get('private', None)
            if private == 'True':
                post.private = True
            elif private == 'False':
                post.private = False
            post.save()
        '''
        Authenticated-only actions.
        save, pin
        '''
        save = request.GET.get('save', None)
        pin = request.GET.get('pin',None)
        print("Save param:", save)
        if request.user.is_authenticated:
            if save == 'True':
                print("Saving this post")
                post.saved_by.add(request.user)
            elif save == 'False':
                print("Canceling save this post")
                post.saved_by.remove(request.user)
            print("This post is saved by:", post.saved_by)

            if request.user.is_staff:
                if pin == 'True':
                    print("Pinning this post")
                    post.pinned = True
                elif pin == 'False':
                    print("Un-pinning this post")
                    post.pinned = False
            post.save()
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
class IndexView(generic.ListView):
    template_name = "posts/index.html"
    model = models.Post
    context_object_name = "posts"
    ordering = "-publish_date"
    paginate_by = 6
    def get_queryset(self):
        # query_set = super(IndexView, self).get_queryset()
        if self.request.user.is_authenticated:
            print("User ",self.request.user," is authenticated ")
            query_set= self.model.objects.visible_to_user(self.request.user)
        else:
            print("Not authenticated")
            query_set= self.model.objects.visible_to_user(-1)
        tag = self.request.GET.get('tag',None)
        author = self.request.GET.get('author',None)

        print(f"Searching tag:{tag},author:{author}")
        if tag:
            query_set = query_set.filter(tags__name=tag)
        if author:
            query_set = query_set.filter(author=author)
        return query_set
class RankingView(generic.TemplateView):
    '''
    rank users by number of published posts or total number of saved of their posts
    '''
    # model = models.UserInfo
    template_name = 'posts/ranking.html'
    # context_object_name = 'profiles'
    # def get_queryset(self):
    #     queryset = super(RankingView, self).get_queryset()
    #     queryset = models.UserInfo.objects.annotate(post_count = Count('user__post'))
    #     return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RankingView, self).get_context_data(object_list=None, **kwargs)
        post_count_queryset = models.UserInfo.objects.annotate(published_count = Count('user__post'))
        context['published_profiles'] = post_count_queryset.order_by('-published_count')
        post_saved_queryset = models.UserInfo.objects.annotate(saved_count = Sum('user__post__saved_by'))
        context['saved_profiles'] = post_saved_queryset.order_by('-saved_count')
        return context
class SearchView(generic.TemplateView):
    template_name = "posts/search.html"
    def get_context_data(self, **kwargs):
        keyword = self.request.GET.get('search')
        '''
        utilizing drf search filter to search for posts 
        '''
        print("Keyword:", keyword)
        context = super(SearchView, self).get_context_data(**kwargs)
        filter = filters.SearchFilter()
        request = Request(self.request)
        if self.request.user.is_authenticated:
            print("User ", self.request.user, " is authenticated ")
            queryset = models.Post. objects.visible_to_user(self.request.user)
        else:
            print("Not authenticated")
            queryset = models.Post.objects.visible_to_user(-1)
        view = PostsAPIView
        results =  filter.filter_queryset(request, queryset, view)
        print(results)
        context['search_results'] = results
        return context
    def get(self, request:HttpRequest, *args, **kwargs):
        return super(SearchView, self).get( request, *args, **kwargs)
class ContactView(generic.TemplateView):
    template_name = "posts/contact.html"

'''DRF API views'''
class PostsAPIView(viewsets.ModelViewSet):
    search_fields = ['title','content','author__username']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    # filter_backends = [DjangoFilterBackend]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    def get_queryset(self):
        '''Hide private posts'''
        queryset = super(PostsAPIView, self).get_queryset()
        return queryset.filter(private=False)
class CommentsAPIView(viewsets.ModelViewSet):
    search_fields = ['comment','user_email','user_name']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
class TagsAPIView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer