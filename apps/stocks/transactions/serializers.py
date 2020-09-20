from django.db import transaction
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.stocks.transactions.models import StockTransaction, UserStockTransaction
from main.models import User
from main.serializers.base import BaseModelSerializer


class StockTransactionSerializer(BaseModelSerializer):
    total_value = MoneyField(max_digits=14, decimal_places=4, read_only=True)
    total_value_currency = serializers.CharField(read_only=True, allow_null=True)
    per_stock_price = MoneyField(max_digits=14, decimal_places=4)
    commission = MoneyField(max_digits=14, decimal_places=4)
    tax = MoneyField(max_digits=14, decimal_places=4)
    user = serializers.UUIDField(write_only=True)
    broker_name = serializers.CharField(write_only=True)

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop('user')
        broker = validated_data.pop('broker_name')
        stock_transaction = super().create(validated_data)

        stock_transaction.full_clean()
        stock_transaction.save()

        try:
            user_obj = User.objects.get(id=user)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        user_stock_transaction = UserStockTransaction.objects.create(
            user=user_obj,
            transaction=stock_transaction,
            broker_name=broker
        )

        user_stock_transaction.full_clean()
        user_stock_transaction.save()

        return stock_transaction

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


class UserStockTransactionSerializer(BaseModelSerializer):
    class Meta:
        model = UserStockTransaction
        fields = [
            'uuid',
            'transaction',
            'user',
            'broker_name'
        ]
