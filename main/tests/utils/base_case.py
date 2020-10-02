import pytz
from django.test import TestCase
from moneyed import Money

from apps.stocks.markets.models import Market, Company, CompanyStock, MarketCompanyStock
from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction, \
    StockSplitTransaction, UserBroker
from main.models import User
from main.settings import TIME_ZONE
from main.tests.faker import faker


class BaseTestCase(TestCase):
    faker = faker

    @classmethod
    def _create_model_instance(cls, object_model, **fields):
        instance = object_model(
            **fields,
            created_by=None
        )

        instance.full_clean()
        instance.save()

        return instance

    @classmethod
    def create_user(cls) -> tuple:
        password = cls.faker.password()

        user = cls._create_model_instance(
            User,
            email=cls.faker.email(),
            password=password,
            is_active=True
        )

        user.set_password(password)
        user.full_clean()
        user.save()

        return user, password

    @classmethod
    def create_superuser(cls) -> tuple:
        user, password = cls.create_user()

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user, password

    @classmethod
    def create_market(cls, market_name=None) -> object:
        if market_name is None:
            market_name = cls.faker.catch_phrase()

        market = cls._create_model_instance(
            Market,
            name=market_name,
        )

        return market

    @classmethod
    def create_company(cls, name=None) -> object:
        if name is None:
            name = cls.faker.company()

        company = cls._create_model_instance(
            Company,
            name=name,
        )

        return company

    @classmethod
    def create_user_broker(cls, user=None, broker_name=None) -> object:
        if user is None:
            user, _ = cls.create_user()

        if broker_name is None:
            broker_name = cls.faker.company()

        user_broker = cls._create_model_instance(
            UserBroker,
            user=user,
            broker_name=broker_name,
        )

        return user_broker

    @classmethod
    def create_company_stock(cls, company=None, symbol=None, details=None) -> object:
        if company is None:
            company = cls.create_company()

        if symbol is None:
            symbol = cls.faker.company_suffix()

        if details is None:
            details = cls.faker.sentence()

        company_stock = cls._create_model_instance(
            CompanyStock,
            company=company,
            symbol=symbol,
            details=details
        )

        return company_stock

    @classmethod
    def create_market_company_stock(cls, market=None, company_stock=None) -> object:
        if market is None:
            market = cls.create_market()

        if company_stock is None:
            company_stock = cls.create_company_stock()

        market_company_stock = cls._create_model_instance(
            MarketCompanyStock,
            market=market,
            company_stock=company_stock
        )

        return market_company_stock

    @classmethod
    def create_stock_transaction(cls, company_stock=None, transaction_type=None, quantity=0, per_stock_price=0,
                                 currency='USD', commission=0, tax=0, date=None, user=None, broker=None) -> object:
        if transaction_type is None:
            transaction_type = cls.faker.stock_transaction_type()

        if company_stock is None:
            company_stock = cls.create_company_stock()

        if quantity <= 0:
            quantity = cls.faker.stock_quantity()

        if per_stock_price <= 0:
            per_stock_price = cls.faker.per_stock_price()

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        if user is None:
            user, _ = cls.create_user()

        if broker is None:
            broker = cls.create_user_broker()

        stock_transaction = cls._create_model_instance(
            StockTransaction,
            type=transaction_type,
            company_stock=company_stock,
            stock_quantity=quantity,
            per_stock_price=Money(per_stock_price, currency=currency),
            commission=Money(commission, currency=currency),
            tax=Money(tax, currency=currency),
            date=date,
            user=user,
            broker=broker
        )

        return stock_transaction

    @classmethod
    def create_cash_dividend_transaction(cls, company_stock=None, dividend=0, commission=0, tax=0,
                                         currency='USD', date=None, user=None, broker=None) -> object:
        if company_stock is None:
            company_stock = cls.create_company_stock()

        if dividend <= 0:
            dividend = cls.faker.dividend()

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        if user is None:
            user, _ = cls.create_user()

        if broker is None:
            broker = cls.create_user_broker()

        cash_dividend_transaction = cls._create_model_instance(
            CashDividendTransaction,
            company_stock=company_stock,
            dividend=Money(dividend, currency=currency),
            commission=Money(commission, currency=currency),
            tax=Money(tax, currency=currency),
            date=date,
            user=user,
            broker=broker
        )

        return cash_dividend_transaction

    @classmethod
    def create_stock_dividend_transaction(cls, company_stock=None, stock_quantity=0,
                                          date=None, user=None, broker=None) -> object:
        if company_stock is None:
            company_stock = cls.create_company_stock()

        if stock_quantity <= 0:
            stock_quantity = cls.faker.stock_quantity()

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        if user is None:
            user, _ = cls.create_user()

        if broker is None:
            broker = cls.create_user_broker()

        stock_dividend_transaction = cls._create_model_instance(
            StockDividendTransaction,
            company_stock=company_stock,
            stock_quantity=stock_quantity,
            date=date,
            user=user,
            broker=broker
        )

        return stock_dividend_transaction

    @classmethod
    def create_stock_split_transaction(cls, company_stock=None, exchange_ratio_from=0,
                                       exchange_ratio_for=0, optional=None, pay_date=None) -> object:
        if company_stock is None:
            company_stock = cls.create_company_stock()

        if exchange_ratio_from <= 0:
            exchange_ratio_from = cls.faker.exchange_ratio()

        if exchange_ratio_for <= 0:
            exchange_ratio_for = cls.faker.exchange_ratio()

        if optional is None:
            optional = cls.faker.boolean()

        if pay_date is None:
            pay_date = cls.faker.date()

        stock_split_transaction = cls._create_model_instance(
            StockSplitTransaction,
            company_stock=company_stock,
            exchange_ratio_from=exchange_ratio_from,
            exchange_ratio_for=exchange_ratio_for,
            optional=optional,
            pay_date=pay_date
        )

        return stock_split_transaction
