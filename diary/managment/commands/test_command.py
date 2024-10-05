from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Тестовая команда"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Тестовая команда успешно работает"))
