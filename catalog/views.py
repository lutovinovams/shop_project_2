from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from catalog.models import Product


class ProductListView(ListView):
    """
    Контроллер для отображения списка товаров на главной странице.
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """
    Контроллер для отображения детальной информации о товаре.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """
    Контроллер для создания нового товара.
    ```"""
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


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
