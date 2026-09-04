from django.contrib import admin
from catalog.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели категорий.
    """
    list_display = ('id', 'name',)
    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели продуктов.
    """
    list_display = ('id', 'name', 'price', 'category', 'created_at',)
    list_filter = ('category', 'created_at',)
    search_fields = ('name', 'description',)
