from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from catalog.models import Product

# Create your views here.

menu = [{'title': "Обратная связь", 'url_name': 'contacts'},
        ]


def index(request):
    """
    Функция для отображения главной страницы приложения.
    """
    return render(request, 'catalog/index.html', {'title': 'Skystore'})


def contacts(request):
    """
    Функция реализует обработку сбора обратной связи от пользователя, который зашел на страницу контактов и отправил
    свои данные для обратной связи.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'Contact information received: User {name} with phone {phone} send message: {message}')
    return render(request, 'catalog/contacts.html', {'menu': menu, 'title': 'Обратная связь'})


class ProductListView(ListView):
    """
    Класс для работы с моделью Продуктов.
    """
    model = Product
    extra_context = {
        'object_list': Product.objects.all(),
        'title': 'Каталог программных продуктов',
    }


class ProductDetailView(DetailView):
    """
    Класс для получения деталей (единиц) модели Продуктов.
    """
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ProductCreateView(CreateView):
    """
    Класс создания новых единиц продуктов для модели Продуктов.
    """
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    """
    Класс для обновления единиц продуктов для модели Продуктов.
    """
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    """
    Класс для удаления единиц продуктов из модели Продуктов.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')


def pageNotFound(request, exception):
    """
    Функция для корректного отображения страницы при ошибке Http404 (pageNotFound).
    Только при mode DEBUG off.
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
