from random import random, choice, uniform

import pytz
from django.test import TestCase
from djmoney.money import Money

from apps.stocks.markets.models import Market, Company, MarketCompany
from apps.stocks.transactions.models import StockTransaction, UserStockTransaction
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
                                 commission=0, tax=0, date=None) -> object:
        if transaction_type is None:
            transaction_type = choice(['BUY', 'SELL'])

        if company is None:
            company = cls.create_company()

        if quantity <= 0:
            quantity = round(uniform(0.01, 100), 4)

        if per_stock_price <= 0:
            per_stock_price = round(uniform(0.01, 10000), 4)

        total_value = round((quantity*per_stock_price)-(commission+tax), 4)

        if transaction_type == 'SELL':
            total_value *= -1

        if date is None:
            date = cls.faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))

        stock_transaction = cls._create_model_instance(
            StockTransaction,
            type=transaction_type,
            company=company,
            stock_quantity=quantity,
            per_stock_price=per_stock_price,
            commission=commission,
            tax=tax,
            total_value=total_value,
            date=date
        )

        return stock_transaction

    @classmethod
    def create_user_stock_transaction(cls, user=None, stock_transaction=None, broker_name=None) -> object:
        if user is None:
            user, _ = cls.create_user()

        if stock_transaction is None:
            stock_transaction = cls.create_stock_transaction()

        if broker_name is None:
            broker_name = cls.faker.company()

        user_stock_transaction = cls._create_model_instance(
            UserStockTransaction,
            user=user,
            transaction=stock_transaction,
            broker_name=broker_name,
        )

        return user_stock_transaction
