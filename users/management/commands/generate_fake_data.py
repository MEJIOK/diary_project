from django.core.management.base import BaseCommand
from faker import Faker

from diary.models import Diary
from users.models import User

fake = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Добавляем аргумент email для указания пользователя
        parser.add_argument(
            "email", type=str, help="Email пользователя, для которого создаются записи"
        )

    def handle(self, *args, **kwargs):
        email = kwargs["email"]  # Получаем переданный email

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Пользователь с email {email} не найден.")
            )
            return

        # Генерация 20 записей
        for _ in range(20):
            title = fake.sentence()
            content = fake.paragraph()

            Diary.objects.create(
                title=title,
                content=content,
                author=user,
                status="no_published",  # Убедитесь, что этот статус допустим для модели
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно сгенерировано 20 записей для пользователя {email}"
            )
        )
