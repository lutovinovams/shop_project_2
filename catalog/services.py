"""
Сервисные функции для оптимизации работы с данными и низкоуровневого кеширования.
"""

from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция, возвращающая список продуктов в указанной категории.
    Реализует низкоуровневое кеширование. Ключ строго: category_{id}.
    """
    # Ключ задан строго по критериям ТЗ
    cache_key = f'category_{category_id}'

    # Пытаемся получить данные из Redis
    products = cache.get(cache_key)

    if products is None:
        # Если данных нет, запрашиваем из БД PostgreSQL
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
        # Задаем TTL на 15 минут (900 секунд)
        cache.set(cache_key, products, timeout=60 * 15)

    return products
