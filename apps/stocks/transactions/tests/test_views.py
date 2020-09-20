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

        self.assertEqual(response.status_code, 200)
        return response

    def __post_stock_transaction_helper(self):
        currency_code = self.faker.currency_code()

        response = self.post(
            f'/api/v1/stocktransactions/',
            data={
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
            },
            auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)
        return currency_code, response

    def test_create_stock_transaction(self):
        currency_code, response = self.__post_stock_transaction_helper()
        transaction_type = response.data['type']
        total_value = Decimal(response.data['total_value'])
        compare = operator.gt if transaction_type == "BUY" else operator.lt

        self.assertEqual(response.data['per_stock_price_currency'], currency_code)
        self.assertEqual(response.data['commission_currency'], currency_code)
        self.assertEqual(response.data['total_value_currency'], currency_code)
        self.assertTrue(compare(total_value, Decimal('0.00')))

    def test_create_stock_transaction_with_user_stock_transaction(self):
        user_stock_transactions_response = self.__get_user_stock_transactions_helper()

        self.assertEqual(len(user_stock_transactions_response.data), 0)

        # Creating stock transaction
        _, stock_transaction_response = self.__post_stock_transaction_helper()
        # After creating stock transaction
        user_stock_transactions_response = self.__get_user_stock_transactions_helper()

        self.assertEqual(len(user_stock_transactions_response.data), 1)
        self.assertEqual(user_stock_transactions_response.data[0]['user'], self.superuser.id)
        self.assertEqual(user_stock_transactions_response.data[0]['transaction'],
                         stock_transaction_response.data['uuid'])

