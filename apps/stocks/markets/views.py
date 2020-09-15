from apps.stocks.markets.models import Market, Company, MarketCompany
from apps.stocks.markets.serializers import MarketSerializer, CompanySerializer, MarketCompanySerializer
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


class MarketCompanyViewSet(ProtectedModelViewSet):
    model = MarketCompany
    queryset = model.objects.none()
    serializer_class = MarketCompanySerializer

    def get_queryset(self):
        return self.model.objects.all()
