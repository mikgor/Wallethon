from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction, \
    StockSplitTransaction, UserBroker
from apps.stocks.transactions.serializers import StockTransactionSerializer, CashDividendTransactionSerializer, \
    StockDividendTransactionSerializer, StockSplitTransactionSerializer, UserBrokerSerializer
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

        # Filter
        if filtered:
            user_stock_transactions = StockTransaction.objects.filter(user=user)\
                .values_list('company_stock__id').distinct().order_by('date')
            latest_date = user_stock_transactions.values_list('date').first()[0]
            earliest_date = user_stock_transactions.values_list('date').last()[0]

            queryset = self.model.objects.filter(
                company_stock__id__in=user_stock_transactions,
                pay_date__lte=earliest_date, pay_date__gte=latest_date)
        else:
            queryset = self.model.objects.all()

        return queryset.order_by('-pay_date')
