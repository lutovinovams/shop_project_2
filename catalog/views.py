from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from catalog.models import Product


class ProductListView(ListView):
    """
    Контроллер-класс для отображения списка товаров на главной странице.
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """
    Контроллер-класс для отображения детальной информации о товаре по его pk.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """
    Контроллер-класс для создания нового товара через форму и сохранения в БД.
    """
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


def contacts(request):
    """
    Контроллер-функция для отображения страницы контактов.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({phone}): {message}")
    return render(request, 'catalog/contacts.html')
