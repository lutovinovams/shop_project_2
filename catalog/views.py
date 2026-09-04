from django.shortcuts import render


def home(request):
    """
    Контроллер для отображения домашней страницы каталога.
    """
    return render(request, 'catalog/home.html')


def contacts(request):
    """
    Контроллер для отображения страницы с контактной информацией.
    Обрабатывает получение данных из формы обратной связи (POST-запрос).
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение: Имя: {name} | Телефон: {phone} | Текст: {message}")

    return render(request, 'catalog/contacts.html')
