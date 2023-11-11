from datetime import datetime, timedelta
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import TimeseriesData, MeasureType


class Command(BaseCommand):
    help = 'Creates data for visual testing.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-points', type=int, default=100,
        )

    # TODO: move to args.
    def _get_random_datetime(self):
        start = datetime(2014, 1, 1, tzinfo=timezone.utc)
        end = datetime(2014, 1, 10, tzinfo=timezone.utc)
        step = timedelta(days=1)
        return start + random.randrange((end - start) // step + 1) * step

    def handle(self, data_points, **options):
        timeseries_data = []
        info = self.stdout.write

        info(f'data_points: {data_points}...')
        # TODO: flush all.
        TimeseriesData.objects.all().delete()

        for m in MeasureType.choices:
            info(f'MeasureType: {m}')
            for _ in range(data_points):
                timeseries_data.append(
                    TimeseriesData(
                        measurement=m[0],
                        value=random.random(),
                        timestamp=self._get_random_datetime()
                    )
                )
        TimeseriesData.objects.bulk_create(timeseries_data)

