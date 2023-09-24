from django.forms import inlineformset_factory, formset_factory

from django.http import HttpResponse, HttpResponseNotFound, request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version, Category


# Create your views here.


class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'SkyStore',
    }


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Обратная связь',
    }

    def post(self, request, *args, **kwargs):
        """
        Функция реализует обработку сбора обратной связи от пользователя, который зашел на страницу контактов и отправил
        свои данные для обратной связи.
        """
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'Contact information received: User {name} with phone {phone} send message: {message}')
        return render(request, self.template_name)


class CategoriesListView(ListView):
    model = Category
    extra_context = {
        'title': 'Все категории',
        'object_list': Category.objects.all()
    }


class ProductListView(ListView):
    """
    Класс для работы с моделью Продуктов.
    """
    model = Product
    extra_context = {
        'object_list': Product.objects.all(),
        'version_list': Version.objects.filter(is_active=True),
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
    form_class = ProductForm
    # fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormSet = formset_factory(VersionForm, extra=1)
        context['version_formset'] = VersionFormSet()
        return context


class ProductUpdateView(UpdateView):
    """
    Класс для обновления единиц продуктов для модели Продуктов.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    # fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)  # extra= 2 выведет 2 формы
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST,
                                                     instance=self.object)  # instance=self.object выводит ещё одну форму
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    """
    Класс для удаления единиц продуктов из модели Продуктов.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class VersionListView(ListView):
    model = Version
    extra_context = {
        'object_list': Version.objects.filter(is_active=True),
        'title': 'Все версии'
    }


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:product_list')


class VersionDetailView(DetailView):
    model = Version

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


def pageNotFound(request, exception):
    """
    Функция для корректного отображения страницы при ошибке Http404 (pageNotFound).
    Только при mode DEBUG off.
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
