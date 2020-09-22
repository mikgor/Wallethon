from apps.stocks.transactions.models import StockTransaction, DividendTransaction
from apps.stocks.transactions.serializers import StockTransactionSerializer, DividendTransactionSerializer
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


class DividendTransactionViewSet(ProtectedModelViewSet):
    model = DividendTransaction
    queryset = model.objects.none()
    serializer_class = DividendTransactionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=user)
