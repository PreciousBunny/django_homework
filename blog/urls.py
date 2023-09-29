from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.decorators.cache import cache_page, never_cache

from blog.apps import BlogConfig
from .views import *


app_name = BlogConfig.name


urlpatterns = [
    path('', never_cache(PostListView.as_view()), name='post_list'),
    path('blog/<slug:slug>', cache_page(60)(PostDetailView.as_view()), name='post_detail'),
    path('create', never_cache(PostCreateView.as_view()), name='post_create'),
    path('update/<slug:slug>', never_cache(PostUpdateView.as_view()), name='post_update'),
    path('delete/<slug:slug>', never_cache(PostDeleteView.as_view()), name='post_delete'),
    path('toggle/<slug:slug>', login_required(toggle_publish), name='toggle_publish'),
    path('allposts', PostAllListView.as_view(), name='all_posts'),
]
