from django.db import models

from main.models import BaseModel


class Market(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class Company(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=64, unique=True)


class MarketCompany(BaseModel):
    market = models.ForeignKey(Market, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)

    class Meta:
        db_table = "stocks_market_company"
