from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from catalog.models import Product

# Create your views here.

menu = [{'title': "Обратная связь", 'url_name': 'contacts'},
        ]


def index(request):
    return render(request, 'catalog/index.html', {'title': 'Skystore'})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'Contact information received: User {name} with phone {phone} send message: {message}')
    return render(request, 'catalog/contacts.html', {'menu': menu, 'title': 'Обратная связь'})


def all_products(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Каталог',
    }

    return render(request, 'catalog/all_products.html', context=context)


def product(request, product_id=None):
    product_item = Product.objects.get(pk=product_id)
    context = {
        'title': product_item.name,
        'description': product_item.description,
        'category': product_item.category,
        'price': product_item.price,
        'create_date': product_item.creation_date,
        'change_date': product_item.modification_date
    }

    return render(request, 'catalog/product.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
