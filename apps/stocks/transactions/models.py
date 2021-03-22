import copy
import time
from decimal import Decimal

import djmoney
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator

from apps.stocks.markets.models import CompanyStock
from main import rules
from main.models import BaseModel, User
from main.settings import STOCK_DECIMAL_PLACES, MONEY_DECIMAL_PLACES


class UserBroker(BaseModel):
    broker_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, models.PROTECT)

    class Meta:
        rules_permissions = {
            "view": rules.is_object_owner,
            "add": rules.is_authenticated,
            "change": rules.is_object_owner,
            "delete": rules.is_object_owner
        }

    def clean(self):
        self.broker_name = self.broker_name.title()


class StockTransaction(BaseModel):
    TRANSACTION_TYPE_BUY = 'BUY'
    TRANSACTION_TYPE_SELL = 'SELL'
    TRANSACTION_TYPE_CHOICES = (
        (TRANSACTION_TYPE_BUY, 'Buy'),
        (TRANSACTION_TYPE_SELL, 'Sell'),
    )

    type = models.CharField(max_length=30, choices=TRANSACTION_TYPE_CHOICES)
    company_stock = models.ForeignKey(CompanyStock, models.PROTECT)
    stock_quantity = models.FloatField(validators=[MinValueValidator(Decimal('0.0000001'))])
    per_stock_price = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, default_currency='USD',
                                 validators=[MinMoneyValidator(Decimal('0.01'))])
    commission = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, default_currency='USD',
                            validators=[MinMoneyValidator(0)])
    tax = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, default_currency='USD',
                     validators=[MinMoneyValidator(0)])
    total_value = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, null=True, blank=True, default_currency=None)
    date = models.DateTimeField()
    user = models.ForeignKey(User, models.CASCADE)
    broker = models.ForeignKey(UserBroker, models.PROTECT)

    class Meta:
        rules_permissions = {
            "view": rules.is_object_owner,
            "add": rules.is_authenticated,
            "change": rules.is_object_owner,
            "delete": rules.is_object_owner
        }

    def clean(self):
        assert self.per_stock_price.currency == self.commission.currency == self.tax.currency, \
                'Currencies must be the same'

        total_value = round((self.stock_quantity * self.per_stock_price), MONEY_DECIMAL_PLACES)
        commissions = self.commission + self.tax

        if self.type == self.TRANSACTION_TYPE_SELL:
            total_value -= commissions
            total_value *= -1

        if self.type == self.TRANSACTION_TYPE_BUY:
            total_value += commissions

        self.total_value = total_value

        if self.type == self.TRANSACTION_TYPE_SELL and self.total_value.amount >= Decimal('0.00'):
            raise ValidationError({'total_value': 'Sell transaction total value must be negative.'})

        if self.type == self.TRANSACTION_TYPE_BUY and self.total_value.amount <= Decimal('0.00'):
            raise ValidationError({'total_value': 'Buy transaction total value must be positive.'})

    def timestamp(self):
        return self.date.timestamp()

    def get_stock_quantity_after_transaction(self, stock_quantity):
        quantity = self.stock_quantity

        if self.type == 'SELL':
            quantity *= -1

        return stock_quantity + quantity


class CashDividendTransaction(BaseModel):
    company_stock = models.ForeignKey(CompanyStock, models.PROTECT)
    dividend = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, default_currency='USD',
                          validators=[MinMoneyValidator(Decimal('0.01'))])
    commission = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, default_currency='USD',
                            validators=[MinMoneyValidator(0)])
    tax = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, default_currency='USD',
                     validators=[MinMoneyValidator(0)])
    total_value = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, null=True, blank=True, default_currency=None)
    date = models.DateTimeField()
    user = models.ForeignKey(User, models.CASCADE)
    broker = models.ForeignKey(UserBroker, models.PROTECT)

    class Meta:
        rules_permissions = {
            "view": rules.is_object_owner,
            "add": rules.is_authenticated,
            "change": rules.is_object_owner,
            "delete": rules.is_object_owner
        }

    def clean(self):
        assert self.dividend.currency == self.commission.currency == self.tax.currency, \
                'Currencies must be the same'

        total_value = round(self.dividend - (self.commission + self.tax), MONEY_DECIMAL_PLACES)

        self.total_value = total_value

        if self.total_value.amount <= Decimal('0.00'):
            raise ValidationError({'total_value': 'Dividend transaction total value must be positive.'})

    def timestamp(self):
        return self.date.timestamp()

    def get_stock_quantity_after_transaction(self, stock_quantity):
        # Can't compare stock and money
        return stock_quantity


class StockDividendTransaction(BaseModel):
    company_stock = models.ForeignKey(CompanyStock, models.PROTECT)
    stock_quantity = models.FloatField(validators=[MinValueValidator(Decimal('0.0000001'))])
    date = models.DateTimeField()
    user = models.ForeignKey(User, models.CASCADE)
    broker = models.ForeignKey(UserBroker, models.PROTECT)

    class Meta:
        rules_permissions = {
            "view": rules.is_object_owner,
            "add": rules.is_authenticated,
            "change": rules.is_object_owner,
            "delete": rules.is_object_owner
        }

    def timestamp(self):
        return self.date.timestamp()

    def get_stock_quantity_after_transaction(self, stock_quantity):
        return stock_quantity + self.stock_quantity


class StockSplitTransaction(BaseModel):
    company_stock = models.ForeignKey(CompanyStock, models.PROTECT)
    exchange_ratio_from = models.FloatField(validators=[MinValueValidator(Decimal('0.0000001'))])
    exchange_ratio_for = models.FloatField(validators=[MinValueValidator(Decimal('0.0000001'))])
    optional = models.BooleanField(default=False)
    pay_date = models.DateField()

    class Meta:
        unique_together = [('company_stock', 'pay_date', 'exchange_ratio_from', 'exchange_ratio_for')]
        db_table = "stocks_transaction_stock_split_transaction"
        rules_permissions = {
            "view": rules.is_authenticated,
            "add": rules.is_superuser,
            "change": rules.is_superuser,
            "delete": rules.is_superuser
        }

    def timestamp(self):
        return int(time.mktime(self.pay_date.timetuple()))

    def get_stock_quantity_after_transaction(self, stock_quantity):
        quantity = stock_quantity * (self.exchange_ratio_for/self.exchange_ratio_from)
        return round(quantity, STOCK_DECIMAL_PLACES)


class SellRelatedBuyStockTransaction(BaseModel):
    buy_stock_transaction = models.ForeignKey(StockTransaction, models.CASCADE)
    sold_quantity = models.FloatField()
    origin_quantity_sold_ratio = models.FloatField()
    profit = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, null=True, blank=True, default_currency=None)

    def __init__(self, sell_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate_profit(sell_value)

    def calculate_profit(self, sell_value):
        if sell_value.currency == self.buy_stock_transaction.total_value.currency:
            costs = self.origin_quantity_sold_ratio*self.buy_stock_transaction.total_value
            self.profit = -sell_value - costs


class SellRelatedStockDividendTransaction(BaseModel):
    stock_dividend_transaction = models.ForeignKey(StockDividendTransaction, models.CASCADE)
    sold_quantity = models.FloatField()
    origin_quantity_sold_ratio = models.FloatField()
    profit = MoneyField(max_digits=14, decimal_places=MONEY_DECIMAL_PLACES, null=True, blank=True, default_currency=None)

    def __init__(self, sell_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate_profit(sell_value)

    def calculate_profit(self, sell_value):
        self.profit = sell_value


class SellStockTransactionSummary(BaseModel):
    sell_transaction = models.ForeignKey(StockTransaction, models.CASCADE)

    def __init__(self, modified_transactions, transactions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sell_related_buy_stock_transactions: [SellRelatedBuyStockTransaction] = []
        self.sell_related_stock_dividend_transactions: [SellRelatedStockDividendTransaction] = []
        self.populate_related_transactions(modified_transactions, transactions)

    def populate_related_transactions(self, modified_transactions, transactions):
        remaining_stock_quantity = self.sell_transaction.stock_quantity
        for modified_transaction in modified_transactions:
            if ((isinstance(modified_transaction, StockTransaction) and modified_transaction.type == 'BUY')
                or isinstance(modified_transaction, StockDividendTransaction))\
                    and modified_transaction.stock_quantity > 0:

                split_ratio = 1
                origin_stock = [transaction for transaction in transactions
                                if transaction.uuid == modified_transaction.uuid][0]
                stock_splits_after_transaction = [transaction for transaction in transactions
                                                  if (isinstance(transaction, StockSplitTransaction)) and
                                                  transaction.timestamp() >= origin_stock.timestamp()]

                for transaction in stock_splits_after_transaction:
                    split_ratio = transaction.get_stock_quantity_after_transaction(split_ratio)

                sold_quantity = modified_transaction.stock_quantity \
                    if remaining_stock_quantity - modified_transaction.stock_quantity > 0 else remaining_stock_quantity

                remaining_stock_quantity = round(remaining_stock_quantity - sold_quantity, STOCK_DECIMAL_PLACES)
                modified_transaction.stock_quantity = \
                    round(modified_transaction.stock_quantity - sold_quantity, STOCK_DECIMAL_PLACES)
                origin_quantity_sold_ratio = \
                    round(sold_quantity / (origin_stock.stock_quantity*split_ratio), STOCK_DECIMAL_PLACES)

                sell_value = self.sell_transaction.total_value * (sold_quantity / self.sell_transaction.stock_quantity)

                if isinstance(modified_transaction, StockDividendTransaction):
                    sell_related_stock_dividend_transaction = SellRelatedStockDividendTransaction(
                        stock_dividend_transaction_id=modified_transaction.id,
                        sold_quantity=sold_quantity,
                        origin_quantity_sold_ratio=origin_quantity_sold_ratio,
                        sell_value=sell_value)
                    self.sell_related_stock_dividend_transactions.append(sell_related_stock_dividend_transaction)

                elif isinstance(modified_transaction, StockTransaction):
                    sell_related_buy_stock_transaction = SellRelatedBuyStockTransaction(
                        buy_stock_transaction_id=modified_transaction.id,
                        sold_quantity=sold_quantity,
                        origin_quantity_sold_ratio=origin_quantity_sold_ratio,
                        sell_value=sell_value)
                    self.sell_related_buy_stock_transactions.append(sell_related_buy_stock_transaction)

                else:
                    pass

                if remaining_stock_quantity <= 0:
                    break


class StockSummary(BaseModel):
    company_stock = models.ForeignKey(CompanyStock, models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transactions = []
        self.modified_transactions = []
        self.buy_stock_transactions = []
        self.sell_stock_transactions_summaries: [SellStockTransactionSummary] = []
        self.cash_dividend_transactions = []
        self.stock_dividend_transactions = []
        self.stock_split_transactions = []
        self.remaining_stock_quantity = 0
        self.cash_dividend_total = 0
        self.stock_dividend_total = 0

    def process_transaction(self, transaction, include_transaction):
        self.transactions.append(copy.copy(transaction))
        self.remaining_stock_quantity = transaction.get_stock_quantity_after_transaction(self.remaining_stock_quantity)

        if isinstance(transaction, StockSplitTransaction):
            for modified_transaction in self.modified_transactions:
                if (isinstance(modified_transaction, StockTransaction) and modified_transaction.type == 'BUY')\
                        or isinstance(modified_transaction, StockDividendTransaction):
                    modified_transaction.stock_quantity =\
                        transaction.get_stock_quantity_after_transaction(modified_transaction.stock_quantity)
            if include_transaction:
                self.stock_split_transactions.append(transaction)

        elif isinstance(transaction, StockTransaction):
            if transaction.type == 'SELL':
                sell_transaction_summary = SellStockTransactionSummary(sell_transaction_id=transaction.id,
                                                                       modified_transactions=self.modified_transactions,
                                                                       transactions=self.transactions)
                if include_transaction:
                    self.sell_stock_transactions_summaries.append(sell_transaction_summary)
            else: # BUY
                if include_transaction:
                    self.buy_stock_transactions.append(transaction)

        elif isinstance(transaction, StockDividendTransaction) and include_transaction:
            self.stock_dividend_transactions.append(transaction)
            self.stock_dividend_total = transaction.get_stock_quantity_after_transaction(self.stock_dividend_total)

        elif isinstance(transaction, CashDividendTransaction) and include_transaction:
            self.cash_dividend_transactions.append(transaction)
            self.cash_dividend_total += transaction.dividend.amount

        else:
            pass

        self.modified_transactions.append(transaction)


class UserBrokerStockSummary(BaseModel):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    user_broker = models.ForeignKey(UserBroker, models.CASCADE)
    currency = models.CharField(max_length=5, choices=djmoney.settings.CURRENCY_CHOICES)

    class Meta:
        rules_permissions = {
            "view": rules.is_object_owner,
            "add": rules.is_authenticated,
            "change": rules.is_object_owner,
            "delete": rules.is_object_owner
        }
