"""
Маршрутизация запросов для модуля управления пользователями users.
"""

from django.urls import path
from users.apps import UsersConfig
from users.views import UserRegisterView, UserLoginView, UserLogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
]
