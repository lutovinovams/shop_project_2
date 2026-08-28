from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем маршруты из приложения catalog
    path('', include('catalog.urls')),
]
