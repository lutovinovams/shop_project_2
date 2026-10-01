"""
Схема маршрутизации для приложения blog (CRUD операции).
"""

from django.urls import path
from blog.apps import BlogConfig
from blog.views import (
    BlogArticleListView, BlogArticleDetailView,
    BlogArticleCreateView, BlogArticleUpdateView, BlogArticleDeleteView
)

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogArticleListView.as_view(), name='article_list'),
    path('<int:pk>/', BlogArticleDetailView.as_view(), name='article_detail'),
    path('create/', BlogArticleCreateView.as_view(), name='article_create'),
    path('edit/<int:pk>/', BlogArticleUpdateView.as_view(), name='article_edit'),
    path('delete/<int:pk>/', BlogArticleDeleteView.as_view(), name='article_delete'),
]
