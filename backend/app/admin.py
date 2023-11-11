from django.contrib import admin

from app.models import MeasurementAlert, TimeseriesData

admin.site.register(TimeseriesData)
admin.site.register(MeasurementAlert)
