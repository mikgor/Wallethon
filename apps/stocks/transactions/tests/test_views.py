import operator
from decimal import Decimal

import pytz

from main.settings import TIME_ZONE
from main.tests.utils.view_case import ViewTestCase


class StockTransactionViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def assert_is_total_value_and_currencies_are_correct(self, data):
        self.assertEqual(data['per_stock_price_currency'], data['commission_currency'])
        self.assertEqual(data['commission_currency'], data['total_value_currency'])

        total_value = round(
            float(data['stock_quantity']) * float(data['per_stock_price'])
            + float(data['commission']) + float(data['tax']), 4)

        if data['type'] == 'SELL':
            total_value *= -1

        self.assertEqual(float(data['total_value']), total_value)

    def __stock_transaction_data_helper(self, user=None):
        if user is None:
            user = self.superuser

        currency_code = self.faker.currency_code()
        data = {
                "type": self.faker.stock_transaction_type(),
                "company": self.create_company().id,
                "stock_quantity": self.faker.stock_quantity(),
                "per_stock_price": self.faker.per_stock_price(),
                "per_stock_price_currency": currency_code,
                "commission": self.faker.commission(),
                "commission_currency": currency_code,
                "tax": self.faker.commission(),
                "tax_currency": currency_code,
                "date": self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                "user": user.id,
                "broker_name": self.faker.company()
            }

        return data

    def __stock_transaction_request_helper(self, method_name: str, endpoint: str = f'/api/v1/stocktransactions/',
                                           data=None, user=None):
        if user is None:
            user = self.superuser

        if data is None:
            data = self.__stock_transaction_data_helper(user=user)

        method = getattr(self, method_name)
        response = method(endpoint, data=data, auth_user=user)

        return response

    def __get_user_stock_transactions_helper(self, user=None):
        return self.__stock_transaction_request_helper(
            method_name='get',
            user=user)

    def __post_stock_transaction_helper(self, user=None):
        return self.__stock_transaction_request_helper(
            method_name='post',
            user=user)

    def __put_stock_transaction_helper(self, transaction_id, data=None, user=None):
        return self.__stock_transaction_request_helper(
            method_name='put',
            endpoint=f'/api/v1/stocktransactions/{transaction_id}/',
            data=data,
            user=user)

    def test_create_stock_transaction(self):
        response = self.__post_stock_transaction_helper()
        transaction_type = response.data['type']
        total_value = Decimal(response.data['total_value'])
        compare = operator.gt if transaction_type == "BUY" else operator.lt

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.superuser.id)
        self.assertTrue(compare(total_value, Decimal('0.00')))
        self.assert_is_total_value_and_currencies_are_correct(response.data)

    def test_update_stock_transaction(self):
        response = self.__post_stock_transaction_helper()
        data = self.__stock_transaction_data_helper()
        data['per_stock_price'] = self.faker.per_stock_price()

        update_response = self.__put_stock_transaction_helper(transaction_id=response.data['uuid'], data=data)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(float(update_response.data['per_stock_price']), data['per_stock_price'])
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Update currency for per_stock_price, commission and tax
        new_currency_code = self.faker.currency_code()
        data['per_stock_price_currency'] = new_currency_code
        data['commission_currency'] = new_currency_code
        data['tax_currency'] = new_currency_code
        update_response = self.__put_stock_transaction_helper(transaction_id=response.data['uuid'], data=data)

        self.assertEqual(update_response.status_code, 200)
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Update currency for per_stock_price
        with self.assertRaises(AssertionError):
            data['per_stock_price_currency'] = self.faker.currency_code()
            self.__put_stock_transaction_helper(transaction_id=response.data['uuid'], data=data)

    def test_stock_transaction_permissions(self):
        user1, _ = self.create_user()
        user2, _ = self.create_user()

        user1_transaction_response = self.__post_stock_transaction_helper(user=user1)
        user2_transaction_response = self.__post_stock_transaction_helper(user=user2)
        user2_transaction2_response = self.__post_stock_transaction_helper(user=user2)

        # User1 updating own transaction
        user1_own_transaction_put_response = self.__put_stock_transaction_helper(
            transaction_id=user1_transaction_response.data['uuid'], user=user1)
        self.assertEqual(user1_own_transaction_put_response.status_code, 200)

        # User2 updating own transaction
        user2_own_transaction_put_response = self.__put_stock_transaction_helper(
            transaction_id=user2_transaction_response.data['uuid'], user=user2)
        self.assertEqual(user2_own_transaction_put_response.status_code, 200)

        # User1 updating user2's transaction
        user1_transaction_put_response = self.__put_stock_transaction_helper(
            transaction_id=user2_transaction_response.data['uuid'], user=user1)
        self.assertEqual(user1_transaction_put_response.status_code, 404)

        # User2 updating user1's transaction
        user2_transaction_put_response = self.__put_stock_transaction_helper(
            transaction_id=user1_transaction_response.data['uuid'], user=user2)
        self.assertEqual(user2_transaction_put_response.status_code, 404)

        # Superuser can update user1's transaction
        superuser_transaction_put_response = self.__put_stock_transaction_helper(
            transaction_id=user1_transaction_response.data['uuid'], user=self.superuser)
        self.assertEqual(superuser_transaction_put_response.status_code, 200)

        # Each user can access only own transactions
        user1_set_response = self.__get_user_stock_transactions_helper(user=user1)
        user2_set_response = self.__get_user_stock_transactions_helper(user=user2)

        self.assertEqual(len(user1_set_response.data), 0)
        self.assertEqual(len(user2_set_response.data), 2)
