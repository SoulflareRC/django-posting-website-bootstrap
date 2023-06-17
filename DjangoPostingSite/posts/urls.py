from django.urls import path,include
from posts.views import apis,posts,comments,messages,profiles,views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers
app_name = "posts"

'''DRF api views'''
router = routers.DefaultRouter()
router.register("posts",apis.PostsAPIView)
router.register("comments",apis.CommentsAPIView)
router.register("tags",apis.TagsAPIView)

urlpatterns = [
    path("index",  views.IndexView.as_view(), name="index"),
    path("ranking",  views. RankingView.as_view(), name="ranking"),
    path("post/<int:pk>", posts.PostView.as_view(), name="post"),
    path("post/create",posts. PostCreateView.as_view(),name="post_create"),
    path("post/<int:pk>/edit",posts. PostEditView.as_view(),name="post_edit"),
    path("post/<int:pk>/delete",posts. PostDeleteView.as_view(),name="post_delete"),
    path("post/<int:pk>/save",posts. PostSaveToggleView.as_view(),name="post_save"),
    path("post/<int:pk>/private",posts. PostPrivateToggleView.as_view(),name="post_private"),
    path("post/<int:pk>/pin",posts. PostPinnedToggleView.as_view(),name="post_pin"),
    path("comment/<int:pk>/delete",comments. CommentDeleteView.as_view(),name="comment_delete"),
    path("message/<int:pk>/delete",messages. MessageDeleteView.as_view(),name="msg_delete"),
    path("user/<int:pk>",  profiles. ProfileView.as_view(), name="user"),
    path("user/<int:pk>/profile",  profiles. ProfileUpdateView.as_view(), name="profile"),
    path("user/<int:pk>/inbox", views. InboxView.as_view(),name="inbox"),
    path('tags/',  views. TagsView.as_view(), name="tags"),
    path('search/',  views. SearchView.as_view(), name="search"),
    path('contact/', views. ContactView.as_view(),name="contact"),
    # # ---- drf apis -----
    path('api/',include(router.urls)),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()