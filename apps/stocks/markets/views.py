from apps.stocks.markets.models import Market, Company, CompanyStock, MarketCompanyStock
from apps.stocks.markets.serializers import MarketSerializer, CompanySerializer, \
    CompanyStockSerializer, MarketCompanyStockSerializer
from main.views import ProtectedModelViewSet


class MarketViewSet(ProtectedModelViewSet):
    model = Market
    queryset = model.objects.none()
    serializer_class = MarketSerializer

    def get_queryset(self):
        return self.model.objects.all()


class CompanyViewSet(ProtectedModelViewSet):
    model = Company
    queryset = model.objects.none()
    serializer_class = CompanySerializer

    def get_queryset(self):
        return self.model.objects.all()


class CompanyStockViewSet(ProtectedModelViewSet):
    model = CompanyStock
    queryset = model.objects.none()
    serializer_class = CompanyStockSerializer

    def get_queryset(self):
        return self.model.objects.all()


class MarketCompanyStockViewSet(ProtectedModelViewSet):
    model = MarketCompanyStock
    queryset = model.objects.none()
    serializer_class = MarketCompanyStockSerializer

    def get_queryset(self):
        return self.model.objects.all()
