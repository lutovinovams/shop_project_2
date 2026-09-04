import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Очищает БД и загружает тестовые данные из фикстур JSON'

    @staticmethod
    def _load_json_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category_data = self._load_json_data('catalog/fixtures/category_data.json')
        product_data = self._load_json_data('catalog/fixtures/product_data.json')

        categories_to_create = []
        for item in category_data:
            categories_to_create.append(
                Category(
                    id=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields']['description']
                )
            )
        Category.objects.bulk_create(categories_to_create)

        products_to_create = []
        for item in product_data:
            products_to_create.append(
                Product(
                    id=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields']['description'],
                    image=item['fields']['image'],
                    category_id=item['fields']['category'],
                    price=item['fields']['price']
                )
            )
        Product.objects.bulk_create(products_to_create)

        self.stdout.write(self.style.SUCCESS('База данных успешно перезаписана тестовыми данными.'))
