from django.db import models

from main.models import BaseModel


class Market(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class Company(BaseModel):
    name = models.CharField(max_length=255)


class CompanyStock(BaseModel):
    company = models.ForeignKey(Company, models.CASCADE)
    symbol = models.CharField(max_length=64)
    details = models.CharField(max_length=255, blank=True, null=True)


class MarketCompanyStock(BaseModel):
    market = models.ForeignKey(Market, models.CASCADE)
    company_stock = models.ForeignKey(CompanyStock, models.CASCADE)

    class Meta:
        unique_together = [('market', 'company_stock')]
        db_table = "stocks_market_company_stock"
