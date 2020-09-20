from decimal import Decimal

from faker.providers import BaseProvider
from random import choice, uniform


class StockTransactionProvider(BaseProvider):
    def stock_transaction_type(self):
        return choice(['BUY', 'SELL'])

    def stock_quantity(self):
        return round(uniform(0.01, 100), 4)

    def per_stock_price(self):
        return round(uniform(0.01, 10000), 4)

    def commission(self):
        return round(uniform(0.01, 10), 4)
