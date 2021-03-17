import datetime
import random
import time

from djmoney.settings import CURRENCY_CHOICES
from faker.providers import BaseProvider
from random import choice, uniform

from main.settings import MONEY_DECIMAL_PLACES
from main.utils import datetime_now


class DateTimeProvider(BaseProvider):
    def date_tuple(self, min_days_difference=1, max_days_difference=365):
        date_from = datetime_now()
        random_number_of_hours = random.randint(min_days_difference*24, max_days_difference*24)
        date_to = date_from + datetime.timedelta(hours=random_number_of_hours)

        return date_from, date_to

    def date_between(self, date_from, date_to):
        hours_between_dates = (time.mktime(date_to.timetuple()) - time.mktime(date_from.timetuple()))//3600
        random_number_of_hours = random.randrange(hours_between_dates)

        return date_from + datetime.timedelta(hours=random_number_of_hours)

    def date_not_between(self, date_from, date_to, after=None):
        if after is None:
            after = random.choice([True, False])

        random_number_of_hours = random.randint(1, 365*3600)
        date = date_to if after else date_from
        sign = 1 if after else -1

        return date + datetime.timedelta(hours=random_number_of_hours*sign)


class CurrencyProvider(BaseProvider):
    def currency_code(self):
        currency_code, _ = choice(CURRENCY_CHOICES)

        return currency_code


class StockTransactionProvider(BaseProvider):
    def stock_transaction_type(self):
        return choice(['BUY', 'SELL'])

    def stock_quantity(self):
        return round(uniform(0.01, 100), MONEY_DECIMAL_PLACES)

    def per_stock_price(self):
        return round(uniform(0.01, 10000), MONEY_DECIMAL_PLACES)

    def commission(self):
        return round(uniform(0.01, 10), MONEY_DECIMAL_PLACES)

    def percent(self):
        return round(uniform(0, 1), MONEY_DECIMAL_PLACES)


class DividendTransactionProvider(BaseProvider):
    def dividend(self):
        return round(uniform(100, 1000), MONEY_DECIMAL_PLACES)


class StockSplitTransactionProvider(BaseProvider):
    def exchange_ratio(self):
        return round(uniform(0.0000001, 1000), 7)
