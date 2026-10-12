"""
Формы регистрации и авторизации кастомных пользователей с Bootstrap-стилизацией.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма для создания учетной записи нового пользователя на основе email.
    Включает обязательные поля электронной почты, пароля и подтверждения пароля.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    """
    Форма для входа в систему по адресу электронной почты и паролю.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
