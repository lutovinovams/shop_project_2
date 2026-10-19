"""
Контроллеры приложения catalog с проверкой прав доступа, защитой объектов
и обработкой страницы контактов.
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from catalog.models import Product
from catalog.forms import ProductForm


class ProductListView(ListView):
    """
    Контроллер-класс для отображения списка товаров на главной странице.
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.has_perm('catalog.can_unpublish_product'):
            return Product.objects.all()
        elif user.is_authenticated:
            return Product.objects.filter(Q(is_published=True) | Q(owner=user))
        return Product.objects.filter(is_published=True)


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
    Контроллер-класс для создания нового товара с автоматической привязкой владельца.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    """
    Контроллер-класс для редактирования товара.
    Доступен только создателю продукта или модератору с соответствующим правом.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
            return obj
        raise PermissionDenied("Вы не являетесь владельцем этого продукта и не имеете прав модератора.")

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    """
    Контроллер-класс для удаления товара.
    Доступен только создателю продукта или модератору с правом удаления.
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if obj.owner == user or user.has_perm('catalog.delete_product'):
            return obj
        raise PermissionDenied("У вас нет прав на удаление этого продукта.")


class ContactsTemplateView(TemplateView):
    """
    Контроллер для отображения статичной страницы контактов с обработкой формы.
    """
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({phone}): {message}")
        return self.get(request, *args, **kwargs)
