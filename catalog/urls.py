"""
Конфигурация маршрутов (URL) для приложения catalog с поддержкой кеширования.
"""

from django.urls import path
from django.views.decorators.cache import cache_page
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    ContactsTemplateView, CategoryProductListView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    # Кеширование детальной страницы на 15 минут
    path('products/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('categories/<int:category_id>/products/', CategoryProductListView.as_view(), name='category_products'),
]
