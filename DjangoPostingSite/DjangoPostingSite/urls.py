"""
URL configuration for DjangoPostingSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views
# from allauth.urls import *
# from allauth.account.urls import *
import fluent_comments.urls
import fluent_comments.templatetags.fluent_comments_tags
urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include('allauth.urls')),

    path("blog/comments/",include('fluent_comments.urls')), # disable this for fluent blogs

    path("martor/",include("martor.urls")),
    path("api/uploader/",views.markdown_uploader,name="markdown_uploader_page"),


    path("posts/",include("posts.urls")),
    path("",lambda request:redirect('posts:index')) # redirect to post index page

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)