from datetime import timedelta, date
from unittest import TestCase

from apps.stocks.utils.utils import get_currency_exchange_rate
from main.utils import datetime_now


class UtilsCurrencyExchangeTestCase(TestCase):
    def test_mid_currency_exchange_rate(self):
        tomorrow = datetime_now() + timedelta(days=1)

        rate = get_currency_exchange_rate('PLN', 'USD', date(2018, 1, 2))
        self.assertEqual(rate, 3.4546)

        rate = get_currency_exchange_rate('PLN', 'EUR', date(2018, 1, 2))
        self.assertEqual(rate, 4.1701)

        rate = get_currency_exchange_rate('PLN', 'USD', date(2020, 9, 21))
        self.assertEqual(rate, 3.7963)

        rate = get_currency_exchange_rate('PLN', 'EUR', date(2020, 9, 21))
        self.assertEqual(rate, 4.4800)

        rate = get_currency_exchange_rate('PLN', 'USD', tomorrow)
        self.assertEqual(rate, None)

        rate = get_currency_exchange_rate('PLN', 'PLN', tomorrow)
        self.assertEqual(rate, None)

        # Weekend days
        rate = get_currency_exchange_rate('PLN', 'USD', date(2020, 9, 19))
        self.assertEqual(rate, None)
        rate = get_currency_exchange_rate('PLN', 'USD', date(2020, 9, 20))
        self.assertEqual(rate, None)
