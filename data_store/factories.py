import factory
import factory.fuzzy

from data_store.models import EquityDataStore


class EquityDataStoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EquityDataStore

    ticker = factory.fuzzy.FuzzyText(length=4)
    exchange = "US"

    open = factory.fuzzy.FuzzyDecimal(0)
    high = factory.fuzzy.FuzzyDecimal(0)
    low = factory.fuzzy.FuzzyDecimal(0)
    close = factory.fuzzy.FuzzyDecimal(0)
    adjusted_close = factory.fuzzy.FuzzyDecimal(0)
    volume = factory.fuzzy.FuzzyDecimal(0)
