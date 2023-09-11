from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from blog.models import Post


# Create your views here.

class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Все записи',  # дополнение к статической информации
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj


class PostCreateView(CreateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[str(self.object.slug)])


def toggle_publish(request, slug):
    """
    Функция переключения поста.
    """
    post_detail = get_object_or_404(Post, slug=slug)
    if post_detail.published:
        post_detail.published = False
    else:
        post_detail.published = True

    post_detail.save()

    return redirect(reverse('blog:post_list'))


class PostAllListView(ListView):
    model = Post
    extra_context = {
        'title': 'Все записи',  # дополнение к статической информации
    }
