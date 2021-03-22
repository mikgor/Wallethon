from itertools import chain

from django.db import transaction
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from apps.stocks.markets.models import CompanyStock
from apps.stocks.markets.serializers import CompanyStockSerializer
from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction, \
    StockSplitTransaction, UserBroker, SellStockTransactionSummary, UserBrokerStockSummary, StockSummary, \
    SellRelatedStockDividendTransaction, SellRelatedBuyStockTransaction
from apps.stocks.transactions.utils.utils import get_user_related_stock_split_transactions, sorted_transactions
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


class BuyStockSellRelatedTransactionSerializer(BaseModelSerializer):
    buy_stock_transaction = StockDividendTransactionSerializer()

    class Meta:
        model = SellRelatedBuyStockTransaction
        fields = [
            'buy_stock_transaction',
            'sold_quantity',
            'origin_quantity_sold_ratio',
        ]


class StockDividendSellRelatedTransactionSerializer(BaseModelSerializer):
    stock_dividend_transaction = StockDividendTransactionSerializer()

    class Meta:
        model = SellRelatedStockDividendTransaction
        fields = [
            'stock_dividend_transaction',
            'sold_quantity',
            'origin_quantity_sold_ratio',
        ]


class SellStockTransactionSummarySerializer(BaseModelSerializer):
    sell_transaction = StockTransactionSerializer()
    sell_related_buy_stock_transactions = serializers.SerializerMethodField()
    sell_related_stock_dividend_transactions = serializers.SerializerMethodField()

    def get_sell_related_buy_stock_transactions(self, obj):
        return BuyStockSellRelatedTransactionSerializer(
            obj.sell_related_buy_stock_transactions, many=True).data

    def get_sell_related_stock_dividend_transactions(self, obj):
        return StockDividendSellRelatedTransactionSerializer(
            obj.sell_related_stock_dividend_transactions, many=True).data

    class Meta:
        model = SellStockTransactionSummary
        fields = [
            'sell_transaction',
            'sell_related_stock_dividend_transactions',
            'sell_related_buy_stock_transactions',
        ]


class StockSummarySerializer(BaseModelSerializer):
    company_stock = CompanyStockSerializer()
    buy_stock_transactions = serializers.SerializerMethodField()
    sell_stock_transactions_summaries = serializers.SerializerMethodField()
    stock_split_transactions = serializers.SerializerMethodField()
    stock_dividend_transactions = serializers.SerializerMethodField()
    cash_dividend_transactions = serializers.SerializerMethodField()
    cash_dividend_total = serializers.SerializerMethodField()
    stock_dividend_total = serializers.SerializerMethodField()
    remaining_stock_quantity = serializers.SerializerMethodField()

    def get_buy_stock_transactions(self, obj):
        return StockTransactionSerializer(obj.buy_stock_transactions, many=True).data

    def get_sell_stock_transactions_summaries(self, obj):
        return SellStockTransactionSummarySerializer(obj.sell_stock_transactions_summaries, many=True).data

    def get_stock_split_transactions(self, obj):
        return StockSplitTransactionSerializer(obj.stock_split_transactions, many=True).data

    def get_stock_dividend_transactions(self, obj):
        return StockDividendTransactionSerializer(obj.stock_dividend_transactions, many=True).data

    def get_cash_dividend_transactions(self, obj):
        return CashDividendTransactionSerializer(obj.cash_dividend_transactions, many=True).data

    def get_cash_dividend_total(self, obj):
        return obj.cash_dividend_total

    def get_stock_dividend_total(self, obj):
        return obj.stock_dividend_total

    def get_remaining_stock_quantity(self, obj):
        return obj.remaining_stock_quantity

    class Meta:
        model = StockSummary
        fields = [
            'company_stock',
            'buy_stock_transactions',
            'sell_stock_transactions_summaries',
            'stock_split_transactions',
            'stock_dividend_transactions',
            'cash_dividend_transactions',
            'cash_dividend_total',
            'stock_dividend_total',
            'remaining_stock_quantity'
        ]


class UserBrokerStockSummarySerializer(BaseModelSerializer):
    data = serializers.SerializerMethodField()
    user_broker = UserBrokerSerializer(read_only=True)
    user_broker_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserBroker.objects.all())

    @transaction.atomic
    def create(self, validated_data):
        validated_data['user_broker'] = validated_data.pop('user_broker_id')
        user_broker_stock_summary = super().create(validated_data)
        user = self.context['request'].user

        # All transactions from beginning are required for calculations, regardless off the date_from
        date_to = user_broker_stock_summary.date_to
        user_stock_transactions = StockTransaction.objects.filter(user=user, date__lte=date_to)
        user_stock_dividend_transactions = StockDividendTransaction.objects.filter(user=user, date__lte=date_to)
        user_cash_dividend_transactions = CashDividendTransaction.objects.filter(user=user, date__lte=date_to)
        user_stock_split_transactions = get_user_related_stock_split_transactions(user, pay_date__lte=date_to)

        transactions = chain(user_stock_transactions[:], user_stock_dividend_transactions[:],
                           user_cash_dividend_transactions[:], user_stock_split_transactions[:])

        self._transactions = sorted_transactions(transactions)

        return user_broker_stock_summary

    def get_data(self, obj):
        user_stocks_summaries = {}

        for transaction in self._transactions:
            stock_id = transaction.company_stock.id

            if stock_id not in user_stocks_summaries:
                user_stocks_summaries[stock_id] = StockSummary(company_stock_id=transaction.company_stock.id)

            include_transaction = obj.date_from.timestamp() <= transaction.timestamp() <= obj.date_to.timestamp()
            user_stocks_summaries[stock_id].process_transaction(transaction=transaction,
                                                                include_transaction=include_transaction)

        serializer = StockSummarySerializer(list(user_stocks_summaries.values()), many=True)

        return serializer.data

    class Meta:
        model = UserBrokerStockSummary
        fields = [
            'uuid',
            'date_from',
            'date_to',
            'user_broker',
            'user_broker_id',
            'currency',
            'data'
        ]
