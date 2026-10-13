"""
Кастомная команда для автоматического создания группы Модераторов с правами по ТЗ.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает ей права из ТЗ'

    def handle(self, *args, **options):
        # Получаем или создаем группу модераторов
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем контент-тип для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Извлекаем нужные разрешения
        can_unpublish = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        can_delete = Permission.objects.get(codename='delete_product', content_type=content_type)

        # Назначаем права группе
        group.permissions.add(can_unpublish, can_delete)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана со всеми правами!'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существовала. Права обновлены.'))
