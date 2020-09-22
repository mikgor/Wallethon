from django.db import transaction
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from apps.stocks.transactions.models import StockTransaction, DividendTransaction
from main.models import User
from main.serializers.base import BaseModelSerializer


class StockTransactionSerializer(BaseModelSerializer):
    total_value = MoneyField(max_digits=14, decimal_places=4, read_only=True)
    total_value_currency = serializers.CharField(read_only=True, allow_null=True)
    per_stock_price = MoneyField(max_digits=14, decimal_places=4)
    commission = MoneyField(max_digits=14, decimal_places=4)
    tax = MoneyField(max_digits=14, decimal_places=4)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    broker_name = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        stock_transaction = super().create(validated_data)

        stock_transaction.full_clean()
        stock_transaction.save()

        return stock_transaction

    @transaction.atomic
    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = StockTransaction
        fields = [
            'uuid',
            'type',
            'company',
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
            'broker_name'
        ]


class DividendTransactionSerializer(BaseModelSerializer):
    total_value = MoneyField(max_digits=14, decimal_places=4, read_only=True)
    total_value_currency = serializers.CharField(read_only=True, allow_null=True)
    dividend = MoneyField(max_digits=14, decimal_places=4)
    commission = MoneyField(max_digits=14, decimal_places=4)
    tax = MoneyField(max_digits=14, decimal_places=4)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    broker_name = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        dividend_transaction = super().create(validated_data)

        dividend_transaction.full_clean()
        dividend_transaction.save()

        return dividend_transaction

    @transaction.atomic
    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        instance.full_clean()
        instance.save()

        return instance

    class Meta:
        model = DividendTransaction
        fields = [
            'uuid',
            'type',
            'company',
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
            'broker_name'
        ]
