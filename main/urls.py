"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from apps.stocks.markets.views import MarketViewSet, CompanyViewSet, MarketCompanyViewSet
from apps.stocks.transactions.views import StockTransactionViewSet, CashDividendTransactionViewSet, \
    StockDividendTransactionViewSet, StockSplitTransactionViewSet
from frontend.views import home_view
from main.views import LoginView, UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'markets', MarketViewSet, basename='markets')
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'marketcompanies', MarketCompanyViewSet, basename='marketcompanies')
router.register(r'stocktransactions', StockTransactionViewSet, basename='stocktransactions')
router.register(r'cashdividendtransactions', CashDividendTransactionViewSet, basename='cashdividendtransactions')
router.register(r'stockdividendtransactions', StockDividendTransactionViewSet, basename='stocktdividendtransactions')
router.register(r'stocksplittransactions', StockSplitTransactionViewSet, basename='stocksplittransactions')

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/', include(router.urls)),
] + staticfiles_urlpatterns()
