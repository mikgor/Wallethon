from faker import Faker
from faker.providers.python import Provider as PythonProvider
from faker.providers.person.pl_PL import Provider as PersonProvider
from faker.providers.company.pl_PL import Provider as CompanyProvider
from faker.providers.lorem.en_US import Provider as LoremProvider
from faker.providers.date_time.en_US import Provider as DateProvider
from faker.providers.misc import Provider as MiscProvider

from main.tests.faker.providers import StockTransactionProvider, CurrencyProvider, DividendTransactionProvider, \
    StockSplitTransactionProvider

Faker.seed(123)

faker = Faker()

faker.add_provider(PythonProvider)
faker.add_provider(PersonProvider)
faker.add_provider(CompanyProvider)
faker.add_provider(LoremProvider)
faker.add_provider(DateProvider)
faker.add_provider(MiscProvider)
faker.add_provider(CurrencyProvider)
faker.add_provider(StockTransactionProvider)
faker.add_provider(DividendTransactionProvider)
faker.add_provider(StockSplitTransactionProvider)
