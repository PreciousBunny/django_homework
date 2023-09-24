from django.contrib.auth.mixins import LoginRequiredMixin
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
        # 'object_list': Product.objects.all(),
        'version_list': Version.objects.filter(is_active=True),
        'title': 'Каталог программных продуктов SkyStore',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        if self.request.user.has_perm('catalog.can_change_product'):
            return queryset
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Класс для получения деталей (единиц) модели Продуктов.
    """
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = self.get_object()
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Класс создания новых единиц продуктов для модели Продуктов.
    """
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        """Метод добавления создателя продукта"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormSet = formset_factory(VersionForm, extra=1)
        context['version_formset'] = VersionFormSet()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс для удаления единиц продуктов из модели Продуктов.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')


def toggle_publish(request, pk):
    """
    Функция переключения публикации программных продуктов.
    """
    product_detail = get_object_or_404(Product, pk=pk)
    if product_detail.is_published:
        product_detail.is_published = False
    else:
        product_detail.is_published = True

    product_detail.save()

    return redirect(reverse('catalog:product_detail', args=[product_detail.pk]))


class ProductAllListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {
        'title': 'Все программные продукты SkyStore',  # дополнение к статической информации
    }


class VersionListView(LoginRequiredMixin, ListView):
    model = Version
    extra_context = {
        'object_list': Version.objects.filter(is_active=True),
        'title': 'Все версии'
    }


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:product_list')


class VersionDetailView(LoginRequiredMixin, DetailView):
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
