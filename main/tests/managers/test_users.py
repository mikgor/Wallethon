from main.models import User
from main.tests.utils.base_case import BaseTestCase
from testfixtures import compare


class UserManagerTestCase(BaseTestCase):
    def __create_action_test_helper(self, method_name: str) -> [User, User]:
        email = self.faker.email()
        password = self.faker.password()
        method = getattr(User.objects, method_name)
        user = method(
            email=email,
            password=password
        )
        requested_user = User.objects.get(email=user.email)
        self.assertTrue(requested_user.is_active)
        compare(requested_user, user)
        return user, requested_user

    def test_create_user_extra_fields(self) -> None:
        user, requested_user = self.__create_action_test_helper("create_user")
        self.assertEqual(requested_user.is_superuser, False)
        self.assertEqual(requested_user.is_staff, False)

    def test_create_superuser_extra_fields(self) -> None:
        user, requested_user = self.__create_action_test_helper("create_superuser")
        self.assertEqual(requested_user.is_superuser, True)
        self.assertEqual(requested_user.is_staff, True)