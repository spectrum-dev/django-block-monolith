from django.db import models
from django.utils.translation import gettext_lazy as _


class EquityDataStore(models.Model):
    class Meta:
        app_label = "data_store"
        unique_together = (("ticker", "datetime", "exchange"),)

    class Exchange(models.TextChoices):
        US = "US", _("United States")
        MY = "MY", _("Malaysia")

    ticker = models.CharField(max_length=21)
    datetime = models.DateTimeField()
    exchange = models.CharField(
        max_length=8,
        choices=Exchange.choices,
    )

    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adjusted_close = models.FloatField()
    volume = models.FloatField()
