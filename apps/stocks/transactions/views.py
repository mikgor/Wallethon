from apps.stocks.transactions.models import StockTransaction, CashDividendTransaction, StockDividendTransaction, \
    StockSplitTransaction
from apps.stocks.transactions.serializers import StockTransactionSerializer, CashDividendTransactionSerializer, \
    StockDividendTransactionSerializer, StockSplitTransactionSerializer
from main.views import ProtectedModelViewSet


class StockTransactionViewSet(ProtectedModelViewSet):
    model = StockTransaction
    queryset = model.objects.none()
    serializer_class = StockTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=user)


class CashDividendTransactionViewSet(ProtectedModelViewSet):
    model = CashDividendTransaction
    queryset = model.objects.none()
    serializer_class = CashDividendTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=user)


class StockDividendTransactionViewSet(ProtectedModelViewSet):
    model = StockDividendTransaction
    queryset = model.objects.none()
    serializer_class = StockDividendTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=user)


class StockSplitTransactionViewSet(ProtectedModelViewSet):
    model = StockSplitTransaction
    queryset = model.objects.none()
    serializer_class = StockSplitTransactionSerializer

    def get_queryset(self):
        return self.model.objects.all()
