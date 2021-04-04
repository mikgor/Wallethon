import operator
from decimal import Decimal

import pytz

from main.settings import TIME_ZONE, STOCK_DECIMAL_PLACES, MONEY_DECIMAL_PLACES
from main.tests.utils.view_case import ViewTestCase
from main.utils import formatted_date, datetime_in_x_days


class UserBrokerViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def __user_broker_data_helper(self, user=None):
        if user is None:
            user = self.superuser

        data = {
            'user': user.id,
            'broker_name': self.faker.company().title()
        }

        return data

    def test_create_user_broker(self):
        data = self.__user_broker_data_helper(user=self.superuser)
        response = self.post(endpoint='/api/v1/userbrokers/', data=data, auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], data['user'])
        self.assertTrue(response.data['broker_name'], data['broker_name'])

    def test_update_user_broker(self):
        response = self.post(endpoint='/api/v1/userbrokers/',
                             data=self.__user_broker_data_helper(), auth_user=self.superuser)

        data = self.__user_broker_data_helper()
        data['broker_name'] = self.faker.company().upper()

        update_response = self.put(endpoint='/api/v1/userbrokers/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['broker_name'], data['broker_name'].title())

        data['broker_name'] = self.faker.company().lower()

        update_response = self.put(endpoint='/api/v1/userbrokers/{id}/'.format(id=response.data['uuid']),
                                   data=data, auth_user=self.superuser)

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['broker_name'], data['broker_name'].title())

    def test_update_user_broker_permissions(self):
        user, _ = self.create_user()

        response = self.post(endpoint='/api/v1/userbrokers/',
                             data=self.__user_broker_data_helper(), auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)

        superuser_get_response = self.get(endpoint='/api/v1/userbrokers/',
                                          data=self.__user_broker_data_helper(), auth_user=self.superuser)

        user_get_response = self.get(endpoint='/api/v1/userbrokers/',
                                     data=self.__user_broker_data_helper(user=user), auth_user=user)

        self.assertEqual(superuser_get_response.status_code, 200)
        self.assertEqual(user_get_response.status_code, 200)

        self.assertEqual(len(superuser_get_response.data), 1)
        self.assertEqual(len(user_get_response.data), 0)


class StockTransactionViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def assert_is_total_value_and_currencies_are_correct(self, data):
        self.assertEqual(data['per_stock_price_currency'], data['commission_currency'])
        self.assertEqual(data['commission_currency'], data['total_value_currency'])

        total_value = float(data['stock_quantity']) * float(data['per_stock_price'])
        commissions = float(data['commission']) + float(data['tax'])

        if data['type'] == 'SELL':
            total_value -= commissions
            total_value *= -1

        if data['type'] == 'BUY':
            total_value += commissions

        self.assertEqual(float(data['total_value']), round(total_value, MONEY_DECIMAL_PLACES))

    def __stock_transaction_data_helper(self, user=None):
        if user is None:
            user = self.superuser

        currency_code = self.faker.currency_code()
        data = {
                'type': self.faker.stock_transaction_type(),
                'company_stock_id': self.create_company_stock().id,
                'stock_quantity': self.faker.stock_quantity(),
                'per_stock_price': self.faker.per_stock_price(),
                'per_stock_price_currency': currency_code,
                'commission': self.faker.commission(),
                'commission_currency': currency_code,
                'tax': self.faker.commission(),
                'tax_currency': currency_code,
                'date': self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                'user': user.id,
                'broker_id': self.create_user_broker().id
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

        total_value = round(float(data['dividend']) - (float(data['commission']) + float(data['tax'])), MONEY_DECIMAL_PLACES)

        self.assertEqual(float(data['total_value']), total_value)

    def __cash_dividend_transaction_data_helper(self, user=None):
        if user is None:
            user = self.superuser

        currency_code = self.faker.currency_code()
        data = {
                'company_stock_id': self.create_company_stock().id,
                'dividend': self.faker.dividend(),
                'dividend_currency': currency_code,
                'commission': self.faker.commission(),
                'commission_currency': currency_code,
                'tax': self.faker.commission(),
                'tax_currency': currency_code,
                'date': self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                'user': user.id,
                'broker_id': self.create_user_broker().id
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
                'company_stock_id': self.create_company_stock().id,
                'stock_quantity': self.faker.stock_quantity(),
                'date': self.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE)),
                'user': user.id,
                'broker_id': self.create_user_broker().id
            }

        return data

    def test_create_stock_dividend_transaction(self):
        data = self.__stock_dividend_transaction_data_helper()
        response = self.post(endpoint='/api/v1/stockdividendtransactions/', data=data, auth_user=self.superuser)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['company_stock']['uuid'], data['company_stock_id'])
        self.assertEqual(response.data['stock_quantity'], data['stock_quantity'])
        self.assertEqual(response.data['date'], formatted_date(data['date']))
        self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['broker']['uuid'], data['broker_id'])

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
                'company_stock_id': self.create_company_stock().id,
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
        self.assertEqual(response.data['company_stock']['uuid'], data['company_stock_id'])
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


class TransactionsSummaryViewSetTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.superuser, _ = self.create_superuser()

    def __transactions_summaries_data_helper(self, date_from=None, date_to=None):
        if date_from is None or date_to is None:
            date_from, date_to = self.faker.date_tuple()

        data = {
                'date_from': date_from,
                'date_to': date_to,
                'user_broker_id': self.create_user_broker().id,
                'currency': self.faker.currency_code(),
            }

        return data

    def __company_stock_transactions_quantity(self, company_stock_id, request_data, transactions):
        return len(
            [transaction for transaction in transactions if transaction.company_stock.id == company_stock_id
             and request_data['date_from'].timestamp() <= transaction.timestamp() <= request_data['date_to'].timestamp()]
                   )

    def __transactions_summaries_response_assert_helper(self, request_data, buy_stock_transactions,
                                                        sell_stock_transactions, cash_dividend_transactions,
                                                        stock_dividend_transactions, stock_split_transactions,
                                                        response):

        self.assertEqual(response.data['date_from'], formatted_date(request_data['date_from']))
        self.assertEqual(response.data['date_to'], formatted_date(request_data['date_to']))
        self.assertEqual(response.data['user_broker']['uuid'], request_data['user_broker_id'])

        for data in response.data['stock_summaries']:
            company_stock_id = data['company_stock']['uuid']
            buy_stock_transactions_quantity = self.__company_stock_transactions_quantity(company_stock_id, request_data,
                                                                                         buy_stock_transactions)
            sell_stock_transactions_quantity = self.__company_stock_transactions_quantity(company_stock_id, request_data,
                                                                                          sell_stock_transactions)
            cash_dividend_transactions_quantity = self.__company_stock_transactions_quantity(company_stock_id, request_data,
                                                                                             cash_dividend_transactions)
            stock_dividend_transactions_quantity = self.__company_stock_transactions_quantity(company_stock_id, request_data,
                                                                                              stock_dividend_transactions)
            stock_split_transactions_quantity = self.__company_stock_transactions_quantity(company_stock_id, request_data,
                                                                                           stock_split_transactions)

            self.assertEqual(len(data['buy_stock_transactions']), buy_stock_transactions_quantity)
            self.assertEqual(len(data['sell_stock_transactions_summaries']), sell_stock_transactions_quantity)
            self.assertEqual(len(data['cash_dividend_transactions_summaries']), cash_dividend_transactions_quantity)
            self.assertEqual(len(data['stock_dividend_transactions']), stock_dividend_transactions_quantity)
            self.assertEqual(len(data['stock_split_transactions']), stock_split_transactions_quantity)

        self.assertEqual(response.status_code, 201)

    def test_create_stocks_transactions_summary_without_transactions(self):
        data = self.__transactions_summaries_data_helper()
        response = self.post(endpoint='/api/v1/transactionssummary/', data=data, auth_user=self.superuser)

        self.__transactions_summaries_response_assert_helper(data, [], [], [], [], [], response)

    def test_stocks_transactions_summary_profit(self):
        date_from, date_to = self.faker.date_tuple()

        quantity_to_buy = self.faker.stock_quantity()
        stock_buy_transaction = self.create_stock_transaction(date=self.faker.date_between(date_from, date_to),
                                                              transaction_type='BUY',
                                                              quantity=quantity_to_buy, user=self.superuser)
        company_stock = stock_buy_transaction.company_stock

        quantity_ratio_to_sell = self.faker.ratio()
        quantity_to_sell = quantity_to_buy * quantity_ratio_to_sell
        stock_sell_transaction = self.create_stock_transaction(date=self.faker.date_between(stock_buy_transaction.date,
                                                                                            date_to),
                                                               company_stock=company_stock,
                                                               quantity=quantity_to_sell,
                                                               transaction_type='SELL',
                                                               user=self.superuser)

        data = self.__transactions_summaries_data_helper(date_from=date_from, date_to=date_to)
        response = self.post(endpoint='/api/v1/transactionssummary/', data=data, auth_user=self.superuser)
        sell_related_buy_stock_transaction = response.data['stock_summaries'][0]['sell_stock_transactions_summaries'][0]['sell_related_buy_stock_transactions'][0]

        income = -stock_sell_transaction.total_value
        costs = stock_buy_transaction.total_value*quantity_ratio_to_sell

        self.assertEqual(round(float(sell_related_buy_stock_transaction['income']), MONEY_DECIMAL_PLACES),
                         round(float(income.amount), MONEY_DECIMAL_PLACES))
        self.assertEqual(round(float(sell_related_buy_stock_transaction['costs']), MONEY_DECIMAL_PLACES),
                         round(float(costs.amount), MONEY_DECIMAL_PLACES))
        self.assertEqual(sell_related_buy_stock_transaction['income_currency'], str(income.currency))
        self.assertEqual(sell_related_buy_stock_transaction['costs_currency'], str(costs.currency))

    def test_create_stocks_transactions_summary(self):
        date_from, date_to = self.faker.date_tuple()

        quantity_to_buy = self.faker.stock_quantity()
        stock_buy_transaction = self.create_stock_transaction(date=self.faker.date_between(date_from, date_to),
                                                              transaction_type='BUY',
                                                              quantity=quantity_to_buy, user=self.superuser)
        company_stock = stock_buy_transaction.company_stock

        quantity_ratio_to_sell = self.faker.ratio()
        quantity_to_sell = quantity_to_buy * quantity_ratio_to_sell
        stock_sell_transaction = self.create_stock_transaction(date=self.faker.date_between(stock_buy_transaction.date,
                                                                                            date_to),
                                                               company_stock=company_stock,
                                                               quantity=quantity_to_sell,
                                                               transaction_type='SELL',
                                                               user=self.superuser)
        stock_sell_transaction_date = stock_sell_transaction.date

        stock_dividend = self.faker.stock_quantity()
        stock_dividend_transaction = self.create_stock_dividend_transaction(date=self.faker.date_between(stock_sell_transaction_date,
                                                                                                         date_to),
                                                                            company_stock=company_stock,
                                                                            stock_quantity=stock_dividend,
                                                                            user=self.superuser)

        cash_dividend = self.faker.dividend()
        cash_dividend_transaction = self.create_cash_dividend_transaction(date=self.faker.date_between(stock_sell_transaction_date,
                                                                                                       date_to),
                                                                          company_stock=company_stock,
                                                                          dividend=cash_dividend,
                                                                          user=self.superuser)

        # This transaction won't be included because it's date is later than date_to
        second_stock_sell_transaction = self.create_stock_transaction(date=self.faker.date_not_between(date_from,
                                                                                                       date_to, True),
                                                                      company_stock=company_stock,
                                                                      quantity=quantity_to_sell,
                                                                      transaction_type='SELL',
                                                                      user=self.superuser)

        remaining_stock_quantity = quantity_to_buy - quantity_to_sell + stock_dividend

        data = self.__transactions_summaries_data_helper(date_from=date_from, date_to=date_to)
        response = self.post(endpoint='/api/v1/transactionssummary/', data=data, auth_user=self.superuser)
        related_transaction = response.data['stock_summaries'][0]['sell_stock_transactions_summaries'][0]['sell_related_buy_stock_transactions'][0]

        self.__transactions_summaries_response_assert_helper(data,
                                                             [stock_buy_transaction],
                                                             [stock_sell_transaction, second_stock_sell_transaction],
                                                             [cash_dividend_transaction], [stock_dividend_transaction],
                                                             [], response)
        self.assertEqual(response.data['stock_summaries'][0]['remaining_stock_quantity'], remaining_stock_quantity)
        self.assertEqual(float(response.data['stock_summaries'][0]['cash_dividend_total']), cash_dividend)
        self.assertEqual(response.data['stock_summaries'][0]['stock_dividend_total'], stock_dividend)
        self.assertEqual(related_transaction['sold_quantity'], quantity_to_sell)
        self.assertEqual(related_transaction['origin_quantity_sold_ratio'], quantity_ratio_to_sell)

    def test_create_stocks_transactions_summary_with_split(self):
        date_from, date_to = self.faker.date_tuple()
        quantity_to_buy = self.faker.stock_quantity()
        stock_buy_transaction = self.create_stock_transaction(date=self.faker.date_between(date_from, date_to),
                                                              transaction_type='BUY',
                                                              quantity=quantity_to_buy, user=self.superuser)
        company_stock = stock_buy_transaction.company_stock

        stock_split_transaction_pay_date = self.faker.date_between(
            datetime_in_x_days(1, date=stock_buy_transaction.date), date_to)
        stock_split_transaction = self.create_stock_split_transaction(pay_date=stock_split_transaction_pay_date,
                                                                      company_stock=company_stock)
        exchange_ratio_from = stock_split_transaction.exchange_ratio_from
        exchange_ratio_for = stock_split_transaction.exchange_ratio_for

        quantity_ratio_to_sell = self.faker.ratio()
        quantity_to_sell = ((quantity_to_buy * exchange_ratio_for) / exchange_ratio_from) * quantity_ratio_to_sell
        stock_sell_transaction = self.create_stock_transaction(date=self.faker.date_between(
                                                                        stock_split_transaction_pay_date, date_to),
                                                               company_stock=company_stock,
                                                               transaction_type='SELL',
                                                               quantity=quantity_to_sell,
                                                               user=self.superuser)

        remaining_stock_quantity =round((stock_buy_transaction.stock_quantity * exchange_ratio_for)
                                        / exchange_ratio_from, STOCK_DECIMAL_PLACES) - quantity_to_sell

        data = self.__transactions_summaries_data_helper(date_from=date_from, date_to=date_to)
        response = self.post(endpoint='/api/v1/transactionssummary/', data=data, auth_user=self.superuser)

        self.__transactions_summaries_response_assert_helper(data,
                                                             [stock_buy_transaction],
                                                             [stock_sell_transaction], [], [], [stock_split_transaction],
                                                             response)
        self.assertEqual(response.data['stock_summaries'][0]['remaining_stock_quantity'], remaining_stock_quantity)
        self.assertEqual(response.data['stock_summaries'][0]['cash_dividend_total'], 0)
        self.assertEqual(response.data['stock_summaries'][0]['stock_dividend_total'], 0)
