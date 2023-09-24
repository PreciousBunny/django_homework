from django.db import models
from django.urls import reverse

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """
    Класс модели Категории продукта.
    """
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}  ( {self.description} )'

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)  # сортировка, '-name' - сортировка в обратном порядке


class Product(models.Model):
    """
    Класс модели Продукта.
    """
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='image/', verbose_name='Изображение', **NULLABLE)
    # category = models.CharField(max_length=150, verbose_name='Категория')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    creation_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    modification_date = models.DateField(verbose_name='Дата последнего изменения', auto_now=True)

    is_active = models.BooleanField(default=True, verbose_name='Доработка программы под ваши требования')

    def __str__(self):
        return f'{self.name}'

    # {self.category}, {self.price}, {self.modification_date}'

    # def get_absolute_url(self):
    #     return reverse('product_detail', kwargs={'pk': self.pk})

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = 'программа'
        verbose_name_plural = 'программы'
        # ordering = ('name',)  # сортировка, '-name' - сортировка в обратном порядке
        ordering = ('name', 'category', 'price', 'modification_date',)


class Version(models.Model):
    """
    Класс модели Версии Продукта.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number_version = models.IntegerField(verbose_name='Номер версии')
    title_version = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(verbose_name='Активная версия', default=True)

    def __str__(self):
        return f'{self.number_version} ({self.product})'

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
