import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from app.models import MeasurementAlert, TimeseriesData, MeasureType

from ml.handle import ask as ml_ask

logger = logging.getLogger(__name__)


class RoomConsumerAbc(WebsocketConsumer):
    def connect(self):
        # gets 'room_name' and open websocket connection
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.close()

    def chat_message(self, event):
        # Receive message from room group
        text = event['message']
        sender = event['sender']

        # broadcast message to all clients in WebSocket
        self.send(text_data=json.dumps({
            'text': text,
            'sender': sender
        }))


class AiChatRoomConsumer(RoomConsumerAbc):

    def _replay_as_ai(self, message: str):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': ml_ask(message),
                'sender': "AI"
            }
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender = text_data_json['sender']

        # Send message to room group.
        #  Thus, it supports the visible chat.
        #  TODO: add support to choose general chat or not.
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text,
                'sender': sender
            }
        )
        self._replay_as_ai(text)


DEAFULT_LAST_VALUES_NUMBER_TO_SEND = 30


class MeasurementAlertRoomConsumer(RoomConsumerAbc):
    LAST_VALUES_NUMBER_TO_SEND = DEAFULT_LAST_VALUES_NUMBER_TO_SEND

    def connect(self):
        super().connect()

        measurement_alerts = MeasurementAlert.objects.filter(active=True)
        logger.info(f'Fetched measurement_alerts: {measurement_alerts}')

        if len(measurement_alerts) != 0:
            # TODO: solve n+1 problem.
            to_send = []  # to dump: [{xData: [], yData: [], xLabel, yLabel}]
            for measurement_alert in measurement_alerts:
                qs = TimeseriesData.objects.filter(measurement=measurement_alert.measurement)
                timeseries_datas = qs[:self.LAST_VALUES_NUMBER_TO_SEND]
                measurement_plot = {
                    'xData': [],
                    'yData': [],
                    'xLabel': "Time",  # TODO: rehardcode.
                    'yLabel': MeasureType(measurement_alert.measurement).label,
                }
                for timeseries_data in timeseries_datas:
                    measurement_plot['xData'].append(timeseries_data.timestamp.timestamp())
                    measurement_plot['yData'].append(timeseries_data.value)

                to_send.append(measurement_plot)

            self.send(text_data=json.dumps(to_send))


class MeasurementsRoomConsumer(RoomConsumerAbc):
    LAST_VALUES_NUMBER_TO_SEND = DEAFULT_LAST_VALUES_NUMBER_TO_SEND

    def connect(self):
        super().connect()

        # TODO: real hack. Create for all measurements deactivated alerts.
        measurement_alerts = MeasurementAlert.objects.all()
        logger.info(f'Fetched measurement_alerts: {measurement_alerts}')

        if len(measurement_alerts) != 0:
            # TODO: solve n+1 problem.
            to_send = []  # to dump: [{xData: [], yData: [], xLabel, yLabel}]
            for measurement_alert in measurement_alerts:
                qs = TimeseriesData.objects.filter(measurement=measurement_alert.measurement).distinct()
                timeseries_datas = qs[:self.LAST_VALUES_NUMBER_TO_SEND]
                measurement_plot = {
                    'xData': [],
                    'yData': [],
                    'hasAlert': measurement_alert.active,
                    'xLabel': "Time",  # TODO: rehardcode.
                    'yLabel': MeasureType(measurement_alert.measurement).label,
                }
                for timeseries_data in timeseries_datas:
                    measurement_plot['xData'].append(timeseries_data.timestamp.timestamp())
                    measurement_plot['yData'].append(timeseries_data.value)

                to_send.append(measurement_plot)

            self.send(text_data=json.dumps(to_send))
