import operator
from decimal import Decimal

import pytz

from main.settings import TIME_ZONE
from main.tests.utils.view_case import ViewTestCase
from main.utils import formatted_date


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
                'type': self.faker.stock_transaction_type(),
                'company': self.create_company().id,
                'stock_quantity': self.faker.stock_quantity(),
                'per_stock_price': self.faker.per_stock_price(),
                'per_stock_price_currency': currency_code,
                'commission': self.faker.commission(),
                'commission_currency': currency_code,
                'tax': self.faker.commission(),
                'tax_currency': currency_code,
                'date': self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                'user': user.id,
                'broker_name': self.faker.company()
            }

        return data

    def test_create_stock_transaction(self):
        response = self.post(endpoint='/api/v1/stocktransactions/',
                             data=self.__stock_transaction_data_helper(), auth_user=self.superuser)
        transaction_type = response.data['type']
        total_value = Decimal(response.data['total_value'])
        compare = operator.gt if transaction_type == 'BUY' else operator.lt

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.superuser.id)
        self.assertTrue(compare(total_value, Decimal('0.00')))
        self.assert_is_total_value_and_currencies_are_correct(response.data)

    def test_update_stock_transaction(self):
        response = self.post(endpoint='/api/v1/stocktransactions/',
                             data=self.__stock_transaction_data_helper(), auth_user=self.superuser)

        data = self.__stock_transaction_data_helper()
        data['per_stock_price'] = self.faker.per_stock_price()

        update_response = self.put(endpoint='/api/v1/stocktransactions/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(float(update_response.data['per_stock_price']), data['per_stock_price'])
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Update currency for per_stock_price, commission and tax
        new_currency_code = self.faker.currency_code()
        data['per_stock_price_currency'] = new_currency_code
        data['commission_currency'] = new_currency_code
        data['tax_currency'] = new_currency_code
        update_response = self.put(endpoint='/api/v1/stocktransactions/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Update currency for per_stock_price
        with self.assertRaises(AssertionError):
            data['per_stock_price_currency'] = self.faker.currency_code()
            self.put(endpoint='/api/v1/stocktransactions/{id}/'.format(id=response.data['uuid']),
                     data=data, auth_user=self.superuser)

    def test_stock_transaction_permissions(self):
        user1, _ = self.create_user()
        user2, _ = self.create_user()

        user1_transaction_response = self.post(endpoint='/api/v1/stocktransactions/',
                                               data=self.__stock_transaction_data_helper(user=user1), auth_user=user1)
        user2_transaction_response = self.post(endpoint='/api/v1/stocktransactions/',
                                               data=self.__stock_transaction_data_helper(user=user2), auth_user=user2)
        self.post(endpoint='/api/v1/stocktransactions/',
                  data=self.__stock_transaction_data_helper(user=user2), auth_user=user2)

        # User1 updating own transaction
        user1_own_transaction_put_response = self.put(
            endpoint='/api/v1/stocktransactions/{id}/'.format(id=user1_transaction_response.data['uuid']),
            data=self.__stock_transaction_data_helper(user=user1), auth_user=user1)
        self.assertEqual(user1_own_transaction_put_response.status_code, 200)

        # User2 updating own transaction
        user2_own_transaction_put_response = self.put(
            endpoint='/api/v1/stocktransactions/{id}/'.format(id=user2_transaction_response.data['uuid']),
            data=self.__stock_transaction_data_helper(user=user2), auth_user=user2)
        self.assertEqual(user2_own_transaction_put_response.status_code, 200)

        # User1 updating user2's transaction
        user1_transaction_put_response = self.put(
            endpoint='/api/v1/stocktransactions/{id}/'.format(id=user2_transaction_response.data['uuid']),
            data=self.__stock_transaction_data_helper(user=user1), auth_user=user1)
        self.assertEqual(user1_transaction_put_response.status_code, 404)

        # User2 updating user1's transaction
        user2_transaction_put_response = self.put(
            endpoint='/api/v1/stocktransactions/{id}/'.format(id=user1_transaction_response.data['uuid']),
            data=self.__stock_transaction_data_helper(user=user2), auth_user=user2)
        self.assertEqual(user2_transaction_put_response.status_code, 404)

        # Superuser can update user1's transaction
        superuser_transaction_put_response = self.put(
            endpoint='/api/v1/stocktransactions/{id}/'.format(id=user1_transaction_response.data['uuid']),
            data=self.__stock_transaction_data_helper(), auth_user=self.superuser)
        self.assertEqual(superuser_transaction_put_response.status_code, 200)

        # Each user can access only own transactions
        user1_set_response = self.get(endpoint='/api/v1/stocktransactions/', auth_user=user1)
        user2_set_response = self.get(endpoint='/api/v1/stocktransactions/', auth_user=user2)
        self.assertEqual(len(user1_set_response.data), 0)
        self.assertEqual(len(user2_set_response.data), 2)


class CashDividendTransactionViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def assert_is_total_value_and_currencies_are_correct(self, data):
        self.assertEqual(data['dividend_currency'], data['commission_currency'])
        self.assertEqual(data['tax_currency'], data['total_value_currency'])

        total_value = round(float(data['dividend']) - (float(data['commission']) + float(data['tax'])), 4)

        self.assertEqual(float(data['total_value']), total_value)

    def __cash_dividend_transaction_data_helper(self, user=None):
        if user is None:
            user = self.superuser

        currency_code = self.faker.currency_code()
        data = {
                'company': self.create_company().id,
                'dividend': self.faker.dividend(),
                'dividend_currency': currency_code,
                'commission': self.faker.commission(),
                'commission_currency': currency_code,
                'tax': self.faker.commission(),
                'tax_currency': currency_code,
                'date': self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                'user': user.id,
                'broker_name': self.faker.company()
            }

        return data

    def test_create_cash_dividend_transaction(self):
        response = self.post(endpoint='/api/v1/cashdividendtransactions/',
                             data=self.__cash_dividend_transaction_data_helper(), auth_user=self.superuser)

        total_value = Decimal(response.data['total_value'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.superuser.id)
        self.assertTrue(total_value >= Decimal('0.00'))
        self.assert_is_total_value_and_currencies_are_correct(response.data)

        data = self.__cash_dividend_transaction_data_helper()
        data['dividend'] = 0.4
        data['commission'] = 0.0
        data['tax'] = 0.1
        response = self.post(endpoint='/api/v1/cashdividendtransactions/', data=data, auth_user=self.superuser)

        self.assertEqual(Decimal(response.data['total_value']), Decimal('0.3'))

    def test_update_cash_dividend_transaction(self):
        response = self.post(endpoint='/api/v1/cashdividendtransactions/',
                             data=self.__cash_dividend_transaction_data_helper(), auth_user=self.superuser)

        data = self.__cash_dividend_transaction_data_helper()
        data['dividend'] = self.faker.dividend()

        update_response = self.put(endpoint='/api/v1/cashdividendtransactions/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(float(update_response.data['dividend']), data['dividend'])
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Update currency for dividend, commission and tax
        new_currency_code = self.faker.currency_code()
        data['dividend_currency'] = new_currency_code
        data['commission_currency'] = new_currency_code
        data['tax_currency'] = new_currency_code
        update_response = self.put(endpoint='/api/v1/cashdividendtransactions/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assert_is_total_value_and_currencies_are_correct(update_response.data)

        # Update currency for dividend
        with self.assertRaises(AssertionError):
            data['dividend_currency'] = self.faker.currency_code()
            self.put(endpoint='/api/v1/cashdividendtransactions/{id}/'.format(id=response.data['uuid']),
                     data=data, auth_user=self.superuser)

    def test_cash_dividend_transaction_permissions(self):
        user1, _ = self.create_user()
        user2, _ = self.create_user()

        user1_transaction_response = self.post(endpoint='/api/v1/cashdividendtransactions/',
                                               data=self.__cash_dividend_transaction_data_helper(user=user1),
                                               auth_user=user1)
        user2_transaction_response = self.post(endpoint='/api/v1/cashdividendtransactions/',
                                               data=self.__cash_dividend_transaction_data_helper(user=user2),
                                               auth_user=user2)

        # User1 updating own transaction
        user1_own_transaction_put_response = self.put(
            endpoint='/api/v1/cashdividendtransactions/{id}/'.format(id=user1_transaction_response.data['uuid']),
            data=self.__cash_dividend_transaction_data_helper(user=user1), auth_user=user1)
        self.assertEqual(user1_own_transaction_put_response.status_code, 200)

        # User2 updating user1's transaction
        user2_transaction_put_response = self.put(
            endpoint='/api/v1/cashdividendtransactions/{id}/'.format(id=user1_transaction_response.data['uuid']),
            data=self.__cash_dividend_transaction_data_helper(user=user2), auth_user=user2)
        self.assertEqual(user2_transaction_put_response.status_code, 404)

        # Superuser can update user2's transaction
        superuser_transaction_put_response = self.put(
            endpoint='/api/v1/cashdividendtransactions/{id}/'.format(id=user2_transaction_response.data['uuid']),
            data=self.__cash_dividend_transaction_data_helper(), auth_user=self.superuser)
        self.assertEqual(superuser_transaction_put_response.status_code, 200)

        # Each user can access only own transactions
        user1_set_response = self.get(endpoint='/api/v1/cashdividendtransactions/', auth_user=user1)
        user2_set_response = self.get(endpoint='/api/v1/cashdividendtransactions/', auth_user=user2)
        self.assertEqual(len(user1_set_response.data), 1)
        self.assertEqual(len(user2_set_response.data), 0)


class StockDividendTransactionViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def __stock_dividend_transaction_data_helper(self, user=None):
        if user is None:
            user = self.superuser

        data = {
                'company': self.create_company().id,
                'stock_quantity': self.faker.stock_quantity(),
                'date': self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                'user': user.id,
                'broker_name': self.faker.company()
            }

        return data

    def test_create_stock_dividend_transaction(self):
        data = self.__stock_dividend_transaction_data_helper()
        response = self.post(endpoint='/api/v1/stockdividendtransactions/', data=data, auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['company'], data['company'])
        self.assertEqual(response.data['stock_quantity'], data['stock_quantity'])
        self.assertEqual(response.data['date'], formatted_date(data['date']))
        self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['broker_name'], data['broker_name'])

    def test_update_stock_dividend_transaction(self):
        response = self.post(endpoint='/api/v1/stockdividendtransactions/',
                             data=self.__stock_dividend_transaction_data_helper(), auth_user=self.superuser)

        data = self.__stock_dividend_transaction_data_helper()
        data['stock_quantity'] = self.faker.stock_quantity()

        update_response = self.put(endpoint='/api/v1/stockdividendtransactions/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(float(update_response.data['stock_quantity']), data['stock_quantity'])


class StockSplitTransactionViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def __stock_split_transaction_data_helper(self):
        data = {
                'company': self.create_company().id,
                'exchange_ratio_from': self.faker.exchange_ratio(),
                'exchange_ratio_for': self.faker.exchange_ratio(),
                'optional': self.faker.boolean(),
                'pay_date': self.faker.date()
            }

        return data

    def test_create_stock_split_transaction(self):
        data = self.__stock_split_transaction_data_helper()
        response = self.post(endpoint='/api/v1/stocksplittransactions/', data=data, auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['company'], data['company'])
        self.assertEqual(response.data['exchange_ratio_from'], data['exchange_ratio_from'])
        self.assertEqual(response.data['exchange_ratio_for'], data['exchange_ratio_for'])
        self.assertEqual(response.data['optional'], data['optional'])
        self.assertEqual(response.data['pay_date'], data['pay_date'])

    def test_update_stock_split_transaction(self):
        response = self.post(endpoint='/api/v1/stocksplittransactions/',
                             data=self.__stock_split_transaction_data_helper(), auth_user=self.superuser)

        data = self.__stock_split_transaction_data_helper()
        data['exchange_ratio_from'] = self.faker.exchange_ratio()
        data['exchange_ratio_for'] = self.faker.exchange_ratio()

        update_response = self.put(endpoint='/api/v1/stocksplittransactions/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['exchange_ratio_from'], data['exchange_ratio_from'])
        self.assertEqual(update_response.data['exchange_ratio_for'], data['exchange_ratio_for'])

    def test_update_stock_split_transaction_permissions(self):
        user, _ = self.create_user()

        response = self.post(endpoint='/api/v1/stocksplittransactions/',
                             data=self.__stock_split_transaction_data_helper(), auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)

        superuser_get_response = self.get(endpoint='/api/v1/stocksplittransactions/',
                                          data=self.__stock_split_transaction_data_helper(), auth_user=self.superuser)

        user_get_response = self.get(endpoint='/api/v1/stocksplittransactions/',
                                     data=self.__stock_split_transaction_data_helper(), auth_user=user)

        self.assertEqual(superuser_get_response.status_code, 200)
        self.assertEqual(user_get_response.status_code, 200)

        user_put_response = self.put(
            endpoint='/api/v1/stocksplittransactions/{id}/'.format(id=response.data['uuid']),
            data=self.__stock_split_transaction_data_helper(), auth_user=user)

        superuser_put_response = self.put(
            endpoint='/api/v1/stocksplittransactions/{id}/'.format(id=response.data['uuid']),
            data=self.__stock_split_transaction_data_helper(), auth_user=self.superuser)

        self.assertEqual(user_put_response.status_code, 403)
        self.assertEqual(superuser_put_response.status_code, 200)
