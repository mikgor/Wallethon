from django.test import TestCase

from main.models import User
from main.tests.faker import faker


class BaseTestCase(TestCase):
    faker = faker

    @classmethod
    def _create_model_instance(cls, object_model, **fields):
        instance = object_model(
            **fields,
            created_by=None
        )

        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    def create_user(cls) -> tuple:
        password = cls.faker.password()

        user = cls._create_model_instance(
            User,
            email=cls.faker.email(),
            password=password,
            is_active=True
        )

        user.set_password(password)
        user.full_clean()
        user.save()

        return user, password

    @classmethod
    def create_superuser(cls) -> tuple:
        user, password = cls.create_user()

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user, password
