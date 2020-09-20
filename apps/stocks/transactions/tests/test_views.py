import operator
from decimal import Decimal

import pytz

from main.settings import TIME_ZONE
from main.tests.utils.view_case import ViewTestCase


class StockTransactionViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def __get_user_stock_transactions_helper(self):
        response = self.get(f'/api/v1/userstocktransactions/', auth_user=self.superuser)

        return response

    def assert_is_total_value_and_currencies_are_correct(self, data):
        self.assertEqual(data['per_stock_price_currency'], data['commission_currency'])
        self.assertEqual(data['commission_currency'], data['total_value_currency'])

        total_value = round(
            float(data['stock_quantity']) * float(data['per_stock_price'])
            + float(data['commission']) + float(data['tax']), 4)

        if data['type'] == 'SELL':
            total_value *= -1

        self.assertEqual(float(data['total_value']), total_value)

    def __stock_transaction_data_helper(self):
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
                "user": self.superuser.id,
                "broker_name": self.faker.company()
            }

        return data

    def __post_stock_transaction_helper(self):
        data = self.__stock_transaction_data_helper()
        response = self.post(
            f'/api/v1/stocktransactions/',
            data=data,
            auth_user=self.superuser)

        return response

    def __put_stock_transaction_helper(self, transaction_id, data=None):
        if data is None:
            data = self.__stock_transaction_data_helper()

        response = self.put(
            f'/api/v1/stocktransactions/{transaction_id}/',
            data=data,
            auth_user=self.superuser)

        return response

    def test_create_stock_transaction(self):
        response = self.__post_stock_transaction_helper()
        transaction_type = response.data['type']
        total_value = Decimal(response.data['total_value'])
        compare = operator.gt if transaction_type == "BUY" else operator.lt

        self.assertEqual(response.status_code, 201)
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

        # Changing currency for per_stock_price, commission, and tax
        new_currency_code = self.faker.currency_code()
        data['per_stock_price_currency'] = new_currency_code
        data['commission_currency'] = new_currency_code
        data['tax_currency'] = new_currency_code
        update_response = self.__put_stock_transaction_helper(transaction_id=response.data['uuid'], data=data)

        self.assertEqual(update_response.status_code, 200)
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Changing currency for per_stock_price
        with self.assertRaises(AssertionError):
            data['per_stock_price_currency'] = self.faker.currency_code()
            update_response = self.__put_stock_transaction_helper(transaction_id=response.data['uuid'], data=data)
            self.assertEqual(update_response.status_code, 403)

    def test_create_stock_transaction_with_user_stock_transaction(self):
        user_stock_transactions_response = self.__get_user_stock_transactions_helper()

        self.assertEqual(len(user_stock_transactions_response.data), 0)

        # Creating stock transaction
        stock_transaction_response = self.__post_stock_transaction_helper()
        # After creating stock transaction
        user_stock_transactions_response = self.__get_user_stock_transactions_helper()

        self.assertEqual(user_stock_transactions_response.status_code, 200)
        self.assertEqual(len(user_stock_transactions_response.data), 1)
        self.assertEqual(user_stock_transactions_response.data[0]['user'], self.superuser.id)
        self.assertEqual(user_stock_transactions_response.data[0]['transaction'],
                         stock_transaction_response.data['uuid'])

