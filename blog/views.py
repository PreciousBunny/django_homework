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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset=queryset)
    #     self.object.view_count += 1
    #     self.object.save()
    #     return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        obj = self.get_object()
        increase = get_object_or_404(Post, pk=obj.pk)  # увеличение количества просмотров
        increase.increase_views()
        return context_data


class PostCreateView(CreateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')
    # fields = ('name', 'slug', 'content', 'image', 'published')
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)


# class PostUpdateView(UpdateView):
#     model = Post
#
#     fields = ('name', 'slug', 'content', 'image', 'published')
#     success_url = reverse_lazy('blog:post_list')
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')
    # fields = ('name', 'slug', 'content', 'image', 'published')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[str(self.object.slug)])
        # return reverse('blog:post_detail', args=[str(self.object.slug)])


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
