from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator

from apps.stocks.markets.models import CompanyStock
from main import rules
from main.models import BaseModel, User


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
    per_stock_price = MoneyField(max_digits=14, decimal_places=4, default_currency='USD',
                                 validators=[MinMoneyValidator(Decimal('0.01'))])
    commission = MoneyField(max_digits=14, decimal_places=4, default_currency='USD',
                            validators=[MinMoneyValidator(0)])
    tax = MoneyField(max_digits=14, decimal_places=4, default_currency='USD',
                     validators=[MinMoneyValidator(0)])
    total_value = MoneyField(max_digits=14, decimal_places=4, null=True, blank=True, default_currency=None)
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

        total_value = round((self.stock_quantity * self.per_stock_price) + (self.commission + self.tax), 4)

        if self.type == self.TRANSACTION_TYPE_SELL:
            total_value *= -1

        self.total_value = total_value

        if self.type == self.TRANSACTION_TYPE_SELL and self.total_value.amount >= Decimal('0.00'):
            raise ValidationError({'total_value': 'Sell transaction total value must be negative.'})

        if self.type == self.TRANSACTION_TYPE_BUY and self.total_value.amount <= Decimal('0.00'):
            raise ValidationError({'total_value': 'Buy transaction total value must be positive.'})


class CashDividendTransaction(BaseModel):
    company_stock = models.ForeignKey(CompanyStock, models.PROTECT)
    dividend = MoneyField(max_digits=14, decimal_places=4, default_currency='USD',
                          validators=[MinMoneyValidator(Decimal('0.01'))])
    commission = MoneyField(max_digits=14, decimal_places=4, default_currency='USD',
                            validators=[MinMoneyValidator(0)])
    tax = MoneyField(max_digits=14, decimal_places=4, default_currency='USD',
                     validators=[MinMoneyValidator(0)])
    total_value = MoneyField(max_digits=14, decimal_places=4, null=True, blank=True, default_currency=None)
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

        total_value = round(self.dividend - (self.commission + self.tax), 4)

        self.total_value = total_value

        if self.total_value.amount <= Decimal('0.00'):
            raise ValidationError({'total_value': 'Dividend transaction total value must be positive.'})


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
