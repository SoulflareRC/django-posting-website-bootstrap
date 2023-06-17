from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.views import generic
from django.http import *
'''Models '''
from django.db.models import Count,Sum,Q
from django.contrib.auth.models import *
from django.contrib import messages

'''DRF'''
from posts import models,serializers
from rest_framework import filters,viewsets
from rest_framework.request import Request
from .apis import PostsAPIView

class TagsView(generic.TemplateView):
    template_name = "posts/tags_page.html"


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
    template_name = 'posts/ranking.html'
    def get_context_data(self, *, object_list=None, **kwargs): # not using listview and query params since it's slow to make request
        context = super(RankingView, self).get_context_data(object_list=None, **kwargs)
        post_saved_queryset = models.UserInfo.objects.annotate(saved_count=Sum('user__post__saved_by'))
        context['saved_profiles'] = post_saved_queryset.order_by('-saved_count').filter(saved_count__gt=0)
        post_count_queryset = models.UserInfo.objects.annotate(published_count = Count('user__post'))
        context['published_profiles'] = post_count_queryset.order_by('-published_count').filter(published_count__gt=0)
        return context

    # model = models.UserInfo
    # context_object_name = 'profiles'
    # def get_queryset(self):
    #     queryset = super(RankingView, self).get_queryset()
    #     order = self.request.GET.get('order')
    #     if order and order == 'saved':
    #         post_saved_queryset = self.model.objects.annotate(saved_count=Sum('user__post__saved_by'))
    #         queryset = post_saved_queryset.order_by('-saved_count').filter(saved_count__gt=0)
    #     else:
    #         '''order defaulted to published'''
    #         post_count_queryset = self.model.objects.annotate(published_count = Count('user__post'))
    #         queryset = post_count_queryset.order_by('-published_count').filter(published_count__gt=0)
    #     return queryset
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(RankingView, self).get_context_data( object_list=None, **kwargs)
    #     order = self.request.GET.get('order')
    #     context['order']=order
    #     return context

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


