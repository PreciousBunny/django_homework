import os
import sys

sys.path.append(os.getcwd())
import json
from django_homework.settings import BASE_DIR
import psycopg2
from django.core.management.base import BaseCommand
from catalog.models import Product, Category


# attention! execute the program with the command: > python manage.py fill

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Привет! Начинаю заполнять БД - Wait few minutes!")

        Product.objects.all().delete()
        Category.objects.all().delete()

        try:
            os.system("python manage.py migrate")
        except Exception:
            print('ОШИБКА: Не правильная команда!')

        with open(BASE_DIR / 'data_category.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            fp.close()

        category_list = []
        for category in data:
            category_list.append(Category(**category["fields"]))
        Category.objects.bulk_create(category_list)

        with open(BASE_DIR / 'data_product.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            fp.close()

        for prod in data:
            name = Category.objects.get(pk=prod["fields"]["category"])
            prod["fields"]["category"] = name

        product_list = []
        for product in data:
            product_list.append(Product(**product["fields"]))
        Product.objects.bulk_create(product_list)
