"""
Контроллеры для управления блоговыми записями (CRUD) на основе Class-Based Views.
Реализует SEO-логику счетчиков, фильтрации контента и перенаправлений.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import BlogArticle


class BlogArticleListView(ListView):
    """
    Контроллер для просмотра списка всех опубликованных статей блога.
    Фильтрует записи по положительному признаку публикации.
    """
    model = BlogArticle
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return BlogArticle.objects.filter(is_published=True)


class BlogArticleDetailView(DetailView):
    """
    Контроллер для просмотра детальной информации одной статьи блога.
    Автоматически увеличивает счетчик просмотров при каждом успешном открытии.
    """
    model = BlogArticle
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogArticleCreateView(CreateView):
    """
    Контроллер для создания новой статьи блога.
    """
    model = BlogArticle
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('blog:article_list')


class BlogArticleUpdateView(UpdateView):
    """
    Контроллер для редактирования существующей статьи блога.
    После редактирования динамически перенаправляет на просмотр этой же статьи.
    """
    model = BlogArticle
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/article_form.html'

    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.object.pk})


class BlogArticleDeleteView(DeleteView):
    """
    Контроллер для удаления статьи из базы данных.
    """
    model = BlogArticle
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('blog:article_list')
