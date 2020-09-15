from apps.stocks.markets.models import Market, Company, MarketCompany
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
            'name',
            'symbol'
        ]


class MarketCompanySerializer(BaseModelSerializer):
    class Meta:
        model = MarketCompany
        fields = [
            'uuid',
            'market',
            'company'
        ]
