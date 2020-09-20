from apps.stocks.transactions.models import StockTransaction, UserStockTransaction
from apps.stocks.transactions.serializers import StockTransactionSerializer, UserStockTransactionSerializer
from main.views import ProtectedModelViewSet


class StockTransactionViewSet(ProtectedModelViewSet):
    model = StockTransaction
    queryset = model.objects.none()
    serializer_class = StockTransactionSerializer

    def get_queryset(self):
        return self.model.objects.all()


class UserStockTransactionViewSet(ProtectedModelViewSet):
    model = UserStockTransaction
    queryset = model.objects.none()
    serializer_class = UserStockTransactionSerializer

    def get_queryset(self):
        return self.model.objects.all()
