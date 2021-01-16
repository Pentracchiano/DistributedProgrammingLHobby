from game.pong.queue.output import QueueOutput
from asgiref.sync import async_to_sync
import threading

from rest_api.models import OngoingMatch
from rest_api.serializers import CompletedMatchSerializer


class PongOutputConsumer:
    def __init__(self, pong_adapter: QueueOutput, channel_layer, group_name: str, match: OngoingMatch):
        self.match = match
        self.group_name = group_name
        self.channel_layer = channel_layer
        self.pong_adapter = pong_adapter

        self.stop = False
        self.thread = threading.Thread(target=self.consume_in_loop)

    def start_consuming(self):
        self.thread.start()

    def stop_consuming(self):
        self.stop = True

    def consume_in_loop(self):
        while not self.stop:
            message = self.pong_adapter.queue.get()
            message_type = message['message_type']
            if message_type == QueueOutput.END:
                self.stop_consuming()

                if message['left_score'] > message['right_score']:
                    winner = self.match.host
                    loser = self.match.challenger
                    winner_score = message['left_score']
                    loser_score = message['right_score']
                else:
                    winner = self.match.challenger
                    loser = self.match.host
                    winner_score = message['right_score']
                    loser_score = message['left_score']

                completed_match = self.match.complete_match(winner, loser, winner_score, loser_score)
                serializer = CompletedMatchSerializer(instance=completed_match)
                # propagating message_type because here i am sending serializer.data and not message.
                end_message_with_type = {'type': 'end_game', 'message_type': QueueOutput.END}
                end_message_with_type.update(serializer.data)

                async_to_sync(self.channel_layer.group_send)(self.group_name, end_message_with_type)
            else:
                message_with_channel_type = {'type': 'game_update'}
                message_with_channel_type.update(message)
                async_to_sync(self.channel_layer.group_send)(self.group_name, message_with_channel_type)

