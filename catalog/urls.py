from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from .views import *


app_name = CatalogConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # http://127.0.0.1:8000/
    path('contacts', ContactView.as_view(), name='contacts'),  # http://127.0.0.1:8000/contacts/
    path('categories', CategoriesListView.as_view(), name='categories_list'),
    path('products', never_cache(ProductListView.as_view()), name='product_list'),
    path('products/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('products/create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('products/update/<int:pk>', never_cache(ProductUpdateView.as_view()), name='product_update'),
    path('products/delete/<int:pk>', never_cache(ProductDeleteView.as_view()), name='product_delete'),
    path('product/toggle/<int:pk>', login_required(toggle_publish), name='toggle_publish'),
    path('allproducts', ProductAllListView.as_view(), name='all_products'),
]
















