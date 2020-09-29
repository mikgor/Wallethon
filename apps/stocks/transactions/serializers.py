from django.db import transaction
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from apps.stocks.markets.models import CompanyStock
from apps.stocks.markets.serializers import CompanyStockSerializer
from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction, \
    StockSplitTransaction, UserBroker
from main.models import User
from main.serializers.base import BaseModelSerializer


class UserBrokerSerializer(BaseModelSerializer):
    broker_name = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))

    @transaction.atomic
    def create(self, validated_data):
        user_broker = super().create(validated_data)

        user_broker.full_clean()
        user_broker.save()

        return user_broker

    @transaction.atomic
    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = UserBroker
        fields = [
            'uuid',
            'broker_name',
            'user',
        ]


class StockTransactionSerializer(BaseModelSerializer):
    company_stock = CompanyStockSerializer(read_only=True)
    company_stock_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CompanyStock.objects.all())
    total_value = MoneyField(max_digits=14, decimal_places=4, read_only=True)
    total_value_currency = serializers.CharField(read_only=True, allow_null=True)
    per_stock_price = MoneyField(max_digits=14, decimal_places=4)
    commission = MoneyField(max_digits=14, decimal_places=4)
    tax = MoneyField(max_digits=14, decimal_places=4)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    broker = UserBrokerSerializer(read_only=True)
    broker_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserBroker.objects.all())

    @transaction.atomic
    def create(self, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        validated_data['broker'] = validated_data.pop('broker_id')
        stock_transaction = super().create(validated_data)

        stock_transaction.full_clean()
        stock_transaction.save()

        return stock_transaction

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        validated_data['broker'] = validated_data.pop('broker_id')
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = StockTransaction
        fields = [
            'uuid',
            'type',
            'company_stock',
            'company_stock_id',
            'stock_quantity',
            'per_stock_price',
            'per_stock_price_currency',
            'commission',
            'commission_currency',
            'tax',
            'tax_currency',
            'total_value',
            'total_value_currency',
            'date',
            'user',
            'broker',
            'broker_id'
        ]


class CashDividendTransactionSerializer(BaseModelSerializer):
    company_stock = CompanyStockSerializer(read_only=True)
    company_stock_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CompanyStock.objects.all())
    total_value = MoneyField(max_digits=14, decimal_places=4, read_only=True)
    total_value_currency = serializers.CharField(read_only=True, allow_null=True)
    dividend = MoneyField(max_digits=14, decimal_places=4)
    commission = MoneyField(max_digits=14, decimal_places=4)
    tax = MoneyField(max_digits=14, decimal_places=4)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    broker = UserBrokerSerializer(read_only=True)
    broker_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserBroker.objects.all())

    @transaction.atomic
    def create(self, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        validated_data['broker'] = validated_data.pop('broker_id')
        dividend_transaction = super().create(validated_data)

        dividend_transaction.full_clean()
        dividend_transaction.save()

        return dividend_transaction

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        validated_data['broker'] = validated_data.pop('broker_id')
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = CashDividendTransaction
        fields = [
            'uuid',
            'company_stock',
            'company_stock_id',
            'dividend',
            'dividend_currency',
            'commission',
            'commission_currency',
            'tax',
            'tax_currency',
            'total_value',
            'total_value_currency',
            'date',
            'user',
            'broker',
            'broker_id'
        ]


class StockDividendTransactionSerializer(BaseModelSerializer):
    company_stock = CompanyStockSerializer(read_only=True)
    company_stock_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CompanyStock.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    broker = UserBrokerSerializer(read_only=True)
    broker_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserBroker.objects.all())

    @transaction.atomic
    def create(self, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        validated_data['broker'] = validated_data.pop('broker_id')
        dividend_transaction = super().create(validated_data)

        dividend_transaction.full_clean()
        dividend_transaction.save()

        return dividend_transaction

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        validated_data['broker'] = validated_data.pop('broker_id')
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = StockDividendTransaction
        fields = [
            'uuid',
            'company_stock',
            'company_stock_id',
            'stock_quantity',
            'date',
            'user',
            'broker',
            'broker_id'
        ]


class StockSplitTransactionSerializer(BaseModelSerializer):
    company_stock = CompanyStockSerializer(read_only=True)
    company_stock_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CompanyStock.objects.all())

    @transaction.atomic
    def create(self, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        dividend_transaction = super().create(validated_data)

        dividend_transaction.full_clean()
        dividend_transaction.save()

        return dividend_transaction

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['company_stock'] = validated_data.pop('company_stock_id')
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = StockSplitTransaction
        fields = [
            'uuid',
            'company_stock',
            'company_stock_id',
            'exchange_ratio_from',
            'exchange_ratio_for',
            'optional',
            'pay_date'
        ]
