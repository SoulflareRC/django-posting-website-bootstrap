from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers
app_name = "posts"

'''DRF api views'''
router = routers.DefaultRouter()
router.register("posts",views.PostsAPIView)
router.register("comments",views.CommentsAPIView)
router.register("tags",views.TagsAPIView)

urlpatterns = [
    path("index", views.IndexView.as_view(), name="index"),
    path("ranking", views.RankingView.as_view(), name="ranking"),
    path("editor", views.EditorView.as_view(), name="editor"),
    path("post/<int:pk>", views.PostView.as_view(), name="post"),
    path("user/<int:pk>", views.ProfileView.as_view(), name="user"),
    path("user/<int:pk>/inbox",views.InboxView.as_view(),name="inbox"),
    path("profile/<int:pk>", views.ProfileUpdateView.as_view(), name="profile"),
    path('tags/', views.TagsView.as_view(), name="tags"),
    path('search/', views.SearchView.as_view(), name="search"),
    path('contact/',views.ContactView.as_view(),name="contact"),
    # # ---- drf apis -----
    path('api/',include(router.urls)),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()