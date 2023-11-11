from django.db import models


class MenuSection(models.Model):
    """
    We want to give a granular access to section in a main menu.
    """

    title = models.CharField("Title", max_length=256)


class MeasureType(models.IntegerChoices):
    GOOG = (1, "GOOG, USD")
    MSFT = (2, "MSFT, USD")
    AAPL = (3, "AAPL, USD")


class TimeseriesData(models.Model):
    measurement = models.IntegerField(choices=MeasureType.choices, db_index=True)
    value = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ('-timestamp',)


class MeasurementAlert(models.Model):
    measurement = models.IntegerField(choices=MeasureType.choices, db_index=True)
    # TODO: uncomment when frontend ready to work with the current actual timeserieses.
    # created = models.DateTimeField()
    # released = models.DateTimeField()
    active = models.BooleanField(default=True, help_text="TODO: It could be deprecated when created and released used.")

    class Meta:
        # TODO: remove this when upper todo solved.
        unique_together = ('measurement', 'active')
