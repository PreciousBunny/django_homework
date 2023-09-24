from django import forms

import django_homework.settings
from catalog.models import *


class FormStyleMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# импорт форм в views.py
class ProductForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('is_active',)  # исключает поле из формы

    def clean_name(self):
        """
        Функция проверяет (валидирует) исключения загрузки продуктов, если в их названии есть запрещенная тематика.
        """
        cleaned_data = self.cleaned_data['name']
        for word in django_homework.settings.FORBIDDEN_WORDS:
            if word in cleaned_data:
                raise forms.ValidationError(f'Запрещенная тематика в названии продукта - "{word}"')
        return cleaned_data

    def clean_description(self):
        """
        Функция проверяет (валидирует) исключения загрузки продуктов, если в их описании есть запрещенная тематика.
        """
        cleaned_data = self.cleaned_data['description']
        for word in django_homework.settings.FORBIDDEN_WORDS:
            if word in cleaned_data:
                raise forms.ValidationError(f'Запрещенная тематика в описании продукта - "{word}"')
        return cleaned_data


class VersionForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
        # exclude = ('is_active',)  # исключает поле из формы

    def clean_is_active(self):
        """
        Проверка валидности только одной активной версии продукта.
        """
        cleaned_data = self.cleaned_data['is_active']

        if cleaned_data and self.instance.product.version_set.filter(is_active=True).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError('Может существовать только одна активная версия!')
        return cleaned_data
