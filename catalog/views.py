"""
Контроллеры для управления продуктами и статичными страницами приложения catalog.
Использует Class-Based Views и декоратор login_required для защиты эндпоинтов.
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from catalog.models import Product
from catalog.forms import ProductForm


class ProductListView(ListView):
    """
    Контроллер-класс для отображения списка товаров на главной странице.
    Эндпоинт полностью доступен не аутентифицированному пользователю по ТЗ.
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    """
    Контроллер-класс для отображения детальной информации о товаре.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    """
    Контроллер-класс для создания нового товара через форму ProductForm.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    """
    Контроллер-класс для редактирования товара с проверкой спам-валидации.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ContactsTemplateView(TemplateView):
    """
    Контроллер-класс для отображения страницы контактов.
    """
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({phone}): {message}")
        return self.get(request, *args, **kwargs)
