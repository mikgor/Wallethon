import pytz
from django.test import TestCase

from apps.stocks.markets.models import Market, Company, MarketCompany
from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction
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
    def create_company(cls, company_name=None, company_symbol=None) -> object:
        if company_name is None:
            company_name = cls.faker.company()

        if company_symbol is None:
            company_symbol = cls.faker.company_suffix()

        company = cls._create_model_instance(
            Company,
            name=company_name,
            symbol=company_symbol
        )

        return company

    @classmethod
    def create_market_company(cls, market=None, company=None) -> object:
        if market is None:
            market = cls.create_market()

        if company is None:
            company = cls.create_company()

        market_company = cls._create_model_instance(
            MarketCompany,
            market=market,
            company=company
        )

        return market_company

    @classmethod
    def create_stock_transaction(cls, company=None, transaction_type=None, quantity=0, per_stock_price=0,
                                 commission=0, tax=0, date=None, user=None, broker_name=None) -> object:
        if transaction_type is None:
            transaction_type = cls.faker.stock_transaction_type()

        if company is None:
            company = cls.create_company()

        if quantity <= 0:
            quantity = cls.faker.stock_quantity()

        if per_stock_price <= 0:
            per_stock_price = cls.faker.per_stock_price()

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        if user is None:
            user, _ = cls.create_user()

        if broker_name is None:
            broker_name = cls.faker.company()

        stock_transaction = cls._create_model_instance(
            StockTransaction,
            type=transaction_type,
            company=company,
            stock_quantity=quantity,
            per_stock_price=per_stock_price,
            commission=commission,
            tax=tax,
            date=date,
            user=user,
            broker_name=broker_name
        )

        return stock_transaction

    @classmethod
    def create_cash_dividend_transaction(cls, company=None, dividend=0, commission=0, tax=0,
                                         date=None, user=None, broker_name=None) -> object:
        if company is None:
            company = cls.create_company()

        if dividend <= 0:
            dividend = cls.faker.dividend()

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        if user is None:
            user, _ = cls.create_user()

        if broker_name is None:
            broker_name = cls.faker.company()

        cash_dividend_transaction = cls._create_model_instance(
            CashDividendTransaction,
            company=company,
            dividend=dividend,
            commission=commission,
            tax=tax,
            date=date,
            user=user,
            broker_name=broker_name
        )

        return cash_dividend_transaction


    @classmethod
    def create_stock_dividend_transaction(cls, company=None, stock_quantity=0,
                                          date=None, user=None, broker_name=None) -> object:
        if company is None:
            company = cls.create_company()

        if stock_quantity <= 0:
            stock_quantity = cls.faker.stock_quantity()

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        if user is None:
            user, _ = cls.create_user()

        if broker_name is None:
            broker_name = cls.faker.company()

        stock_dividend_transaction = cls._create_model_instance(
            StockDividendTransaction,
            company=company,
            stock_quantity=stock_quantity,
            date=date,
            user=user,
            broker_name=broker_name
        )

        return stock_dividend_transaction
