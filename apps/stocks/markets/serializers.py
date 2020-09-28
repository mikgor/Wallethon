from apps.stocks.markets.models import Market, Company, MarketCompanyStock, CompanyStock
from main.serializers.base import BaseModelSerializer


class MarketSerializer(BaseModelSerializer):
    class Meta:
        model = Market
        fields = [
            'uuid',
            'name'
        ]


class CompanySerializer(BaseModelSerializer):
    class Meta:
        model = Company
        fields = [
            'uuid',
            'name'
        ]


class CompanyStockSerializer(BaseModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = CompanyStock
        fields = [
            'uuid',
            'company',
            'symbol',
            'details'
        ]


class MarketCompanyStockSerializer(BaseModelSerializer):
    company_stock = CompanyStockSerializer()

    class Meta:
        model = MarketCompanyStock
        fields = [
            'uuid',
            'market',
            'company_stock'
        ]
