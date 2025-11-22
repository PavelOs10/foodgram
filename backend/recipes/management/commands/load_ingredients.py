import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Загрузка ингредиентов из CSV файла'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'ingredients.csv')

        print(f"Ищу файл здесь: {file_path}")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл не найден! Проверь путь: {file_path}'))
            return

        try:
            with open(file_path, encoding='utf-8') as f:
                reader = csv.reader(f)
                ingredients_to_create = []
                for row in reader:
                   
                    ingredients_to_create.append(
                        Ingredient(
                            name=row[0], 
                            measurement_unit=row[1]
                        )
                    )
                
                Ingredient.objects.bulk_create(ingredients_to_create, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла: {e}'))