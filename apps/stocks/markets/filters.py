from rest_framework_filters import filters, FilterSet
from apps.stocks.markets.models import CompanyStock


class CompanyStockFilter(FilterSet):
    symbol = filters.CharFilter(field_name='symbol', distinct=True)

    class Meta:
        model = CompanyStock
        fields = {
            'symbol': ['exact', 'startswith'],
        }
