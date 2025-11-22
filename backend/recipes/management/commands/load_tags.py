from django.core.management.base import BaseCommand
from recipes.models import Tag

class Command(BaseCommand):
    help = 'Создание стандартных тегов'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#49B64E', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#8775D2', 'slug': 'dinner'}
        ]

        for tag in data:
            obj, created = Tag.objects.get_or_create(
                slug=tag['slug'],
                defaults={'name': tag['name'], 'color': tag['color']}
            )
            if created:
                print(f'Создан тег: {tag["name"]}')
            else:
                print(f'Тег уже существует: {tag["name"]}')

        self.stdout.write(self.style.SUCCESS('Все теги загружены!'))