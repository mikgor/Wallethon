from djmoney.settings import CURRENCY_CHOICES
from faker.providers import BaseProvider
from random import choice, uniform


class CurrencyProvider(BaseProvider):
    def currency_code(self):
        currency_code, _ = choice(CURRENCY_CHOICES)

        return currency_code


class StockTransactionProvider(BaseProvider):
    def stock_transaction_type(self):
        return choice(['BUY', 'SELL'])

    def stock_quantity(self):
        return round(uniform(0.01, 100), 4)

    def per_stock_price(self):
        return round(uniform(0.01, 10000), 4)

    def commission(self):
        return round(uniform(0.01, 10), 4)


class DividendTransactionProvider(BaseProvider):
    def dividend(self):
        return round(uniform(100, 1000), 4)


class StockSplitTransactionProvider(BaseProvider):
    def exchange_ratio(self):
        return round(uniform(0.0000001, 1000), 7)
