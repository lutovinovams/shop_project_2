"""
Контроллеры для обработки процессов регистрации, авторизации и выхода пользователей.
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from users.forms import UserRegisterForm, UserLoginForm


class UserRegisterView(CreateView):
    """
    Контроллер создания профиля пользователя с отправкой приветственного email.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message='Здравствуйте! Спасибо за регистрацию на нашей платформе интернет-магазина.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Контроллер для аутентификации существующих пользователей.
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    """
    Контроллер для завершения текущей сессии пользователя.
    """
    next_page = reverse_lazy('catalog:product_list')
