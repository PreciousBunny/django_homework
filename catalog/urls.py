from django.urls import path, re_path
from catalog.apps import CatalogConfig
from .views import *


app_name = CatalogConfig.name


urlpatterns = [
    path('', index, name='home'),  # http://127.0.0.1:8000/
    path('contacts/', contacts, name='contacts'),  # http://127.0.0.1:8000/contacts/
    path('products/', all_products, name='all_products'),
    path('products/<int:product_id>/', product, name='product'),
]