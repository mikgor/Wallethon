from apps.stocks.transactions.models import StockTransaction
from apps.stocks.transactions.serializers import StockTransactionSerializer
from main.views import ProtectedModelViewSet


class StockTransactionViewSet(ProtectedModelViewSet):
    model = StockTransaction
    queryset = model.objects.none()
    serializer_class = StockTransactionSerializer

    def get_queryset(self):
        return self.model.objects.all()
