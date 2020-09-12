from datetime import datetime
from main.settings import REST_KNOX
from main.tests.utils.view_case import ViewTestCase
from main.utils import datetime_now


class AuthViewsTestCase(ViewTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user, cls.user_password = cls.create_user()

    def __login_post_helper(self, **data):
        if not data:
            data = {
                'username': self.user.email,
                'password': self.user_password
            }

        return self.post('/api/v1/login/', data)

    def test_create_user(self):
        user, password = self.create_superuser()
        response = self.post('/api/v1/users/', data={
            'email': self.faker.email()
        }, auth_user=user)

        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.__login_post_helper()

        now = datetime_now()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            datetime.strptime(response.data['expiry'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(microsecond=0),
            now.replace(microsecond=0, tzinfo=None) + REST_KNOX['TOKEN_TTL']
        )

    def test_login_invalid_credentials(self):
        username = self.user.email
        password = self.user_password

        invalid_username_response = self.__login_post_helper(**{
            'username': password,
            'password': password
        })

        invalid_password_response = self.__login_post_helper(**{
            'username': username,
            'password': username
        })

        invalid_credentials_response = self.__login_post_helper(**{
            'username': '', 'password': ''
        })

        self.assertEqual(invalid_username_response.status_code, 400)
        self.assertEqual(invalid_password_response.status_code, 400)
        self.assertEqual(invalid_credentials_response.status_code, 400)
