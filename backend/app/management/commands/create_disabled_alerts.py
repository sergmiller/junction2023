# docker exec -ti $(docker ps --filter expose=8000 -q) sh -c "python manage.py create_disabled_alerts"
from django.core.management.base import BaseCommand

from app.models import MeasureType, MeasurementAlert


class Command(BaseCommand):
    help = 'Todo.'

    def handle(self, **options):
        info = self.stdout.write

        #  TODO: flushed =(
        MeasurementAlert.objects.all().delete()

        for c in MeasureType.choices:
            MeasurementAlert.objects.create(active=False, measurement=c[0])




