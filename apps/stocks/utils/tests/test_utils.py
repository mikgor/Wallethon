from datetime import date
from unittest import TestCase

from apps.stocks.utils.utils import get_currency_exchange_rate
from main.utils import datetime_in_x_days


class UtilsCurrencyExchangeTestCase(TestCase):
    def test_mid_currency_exchange_rate(self):
        tomorrow = datetime_in_x_days(1)

        rate = get_currency_exchange_rate('USD', 'PLN', date(2018, 1, 2))
        self.assertEqual(rate, 3.4546)

        rate = get_currency_exchange_rate('EUR', 'PLN', date(2018, 1, 2))
        self.assertEqual(rate, 4.1701)

        rate = get_currency_exchange_rate('USD', 'PLN', date(2020, 9, 21))
        self.assertEqual(rate, 3.7963)

        rate = get_currency_exchange_rate('EUR', 'PLN', date(2020, 9, 21))
        self.assertEqual(rate, 4.4800)

        rate = get_currency_exchange_rate('USD', 'PLN', tomorrow)
        self.assertEqual(rate, None)

        rate = get_currency_exchange_rate('PLN', 'PLN', tomorrow)
        self.assertEqual(rate, None)

        # Weekend days
        rate = get_currency_exchange_rate('USD', 'PLN', date(2020, 9, 19))
        self.assertEqual(rate, None)
        rate = get_currency_exchange_rate('USD', 'PLN', date(2020, 9, 20))
        self.assertEqual(rate, None)
