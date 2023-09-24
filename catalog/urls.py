from django.urls import path, re_path
from catalog.apps import CatalogConfig
from .views import *


app_name = CatalogConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # http://127.0.0.1:8000/
    path('contacts', ContactView.as_view(), name='contacts'),  # http://127.0.0.1:8000/contacts/
    path('categories', CategoriesListView.as_view(), name='categories_list'),
    path('products', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
]
















