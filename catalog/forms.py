"""
Формы для управления моделями приложения catalog с кастомной валидацией
и автоматической стилизацией полей под дизайн платформы.
"""

from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов с защитой от спама,
    проверкой цены и автоматической стилизацией элементов через Bootstrap-классы.
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """
        Конструктор формы. Автоматически применяет стили платформы ко всем полям,
        выделяя чекбокс как отдельный элемент формы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def _validate_forbidden_words(self, text):
        """
        Вспомогательный метод для поиска запрещенных слов в любом регистре.
        """
        if text:
            text_lower = text.lower()
            for word in FORBIDDEN_WORDS:
                if word in text_lower:
                    raise ValidationError(f'Использование слова "{word}" запрещено правилами сайта.')
        return text

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return self._validate_forbidden_words(name)

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return self._validate_forbidden_words(description)

    def clean_price(self):
        """
        Кастомная валидация для проверки, что цена продукта не может быть отрицательной.
        """
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной.')
        return price
