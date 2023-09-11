from django.urls import path, re_path
from blog.apps import BlogConfig
from .views import *


app_name = BlogConfig.name


urlpatterns = [
    path('blog', PostListView.as_view(), name='post_list'),
    path('blog/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('create', PostCreateView.as_view(), name='post_create'),
    path('blog/update/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    path('blog/delete/<slug:slug>', PostDeleteView.as_view(), name='post_delete'),
    path('blog/toggle/<slug:slug>', toggle_publish, name='toggle_publish'),
    path('blog/allposts', PostAllListView.as_view(), name='all_posts'),
]
