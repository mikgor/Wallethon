import datetime

import djmoney
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction, \
    StockSplitTransaction, UserBroker
from apps.stocks.transactions.serializers import StockTransactionSerializer, CashDividendTransactionSerializer, \
    StockDividendTransactionSerializer, StockSplitTransactionSerializer, UserBrokerSerializer
from apps.stocks.utils.utils import get_currency_exchange_rate
from main.views import ProtectedModelViewSet


class UserBrokerViewSet(ProtectedModelViewSet):
    model = UserBroker
    queryset = model.objects.none()
    serializer_class = UserBrokerSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(user=user)

        return queryset


class StockTransactionViewSet(ProtectedModelViewSet):
    model = StockTransaction
    queryset = model.objects.none()
    serializer_class = StockTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(user=user)
        return queryset.order_by('-date')


class CashDividendTransactionViewSet(ProtectedModelViewSet):
    model = CashDividendTransaction
    queryset = model.objects.none()
    serializer_class = CashDividendTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(user=user)
        return queryset.order_by('-date')


class StockDividendTransactionViewSet(ProtectedModelViewSet):
    model = StockDividendTransaction
    queryset = model.objects.none()
    serializer_class = StockDividendTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(user=user)

        return queryset.order_by('-date')


class StockSplitTransactionViewSet(ProtectedModelViewSet):
    model = StockSplitTransaction
    queryset = model.objects.none()
    serializer_class = StockSplitTransactionSerializer

    def get_queryset(self):
        user = self.request.user
        filtered = self.request.query_params.get('filtered')

        # Return only stock splits when user has or had any quantity of splitted stock
        if filtered:
            user_stock_transactions = StockTransaction.objects.filter(user=user)
            user_stock_dividend_transactions = StockDividendTransaction.objects.filter(user=user)

            # {'stock_id': total_stock_quantity}
            stocks_amounts = {}

            # Sum user's buy and sell (with minus sign) transactions' quantities
            for transaction in user_stock_transactions:
                stock_id = transaction.company_stock.id
                stock_quantity = transaction.stock_quantity

                if transaction.type == 'SELL':
                    stock_quantity *= -1

                if stock_id in stocks_amounts:
                    stocks_amounts[stock_id] += stock_quantity
                else:
                    stocks_amounts[stock_id] = stock_quantity

            # Sum user's dividend transactions' quantities
            for dividend_transaction in user_stock_dividend_transactions:
                stock_id = dividend_transaction.company_stock.id
                if stock_id in stocks_amounts:
                    stocks_amounts[stock_id] += dividend_transaction.stock_quantity
                else:
                    stocks_amounts[stock_id] = dividend_transaction.stock_quantity

            filtered_stocks_amounts = {stock: amount for (stock, amount) in stocks_amounts.items()}

            queryset = self.model.objects.filter(company_stock__id__in=filtered_stocks_amounts.keys())
        else:
            queryset = self.model.objects.all()

        return queryset.order_by('-pay_date')


class ExchangeView(APIView):
    http_method_names = ['get']

    def get(self, request):
        currency_from = self.request.query_params.get('from')
        currency_to = self.request.query_params.get('to')
        currency_date = datetime.datetime.strptime(self.request.query_params.get('date'), '%Y-%m-%d').date()

        return Response(get_currency_exchange_rate(currency_from, currency_to, currency_date))


class CurrenciesView(APIView):
    http_method_names = ['get']

    def get(self, request):
        currency_choices = djmoney.settings.CURRENCY_CHOICES
        currencies = []
        for symbol, name in currency_choices:
            currencies.append({'symbol': symbol, 'name': name})

        return Response(currencies)
