import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
import urllib.parse

from django.db import transaction, IntegrityError

from game.pong.controller import Controller
from game.pong.queue.input import QueueInput
from game.pong.queue.output import QueueOutput
from game.pong_output_consumer import PongOutputConsumer
from rest_api.models import OngoingMatch, CompletedMatch
from game.pong.paddle import PaddleCommand


games_to_input_handler = {}


class GameConsumer(JsonWebsocketConsumer):
    INVALID_COMMAND = 0
    NO_COMMAND = 1
    CHALLENGER_NOT_READY = 2

    MAX_INPUT_QUEUE_SIZE = 10
    MAX_OUTPUT_QUEUE_SIZE = 10

    COMMANDS = {
        'up': PaddleCommand.UP,
        'down': PaddleCommand.DOWN,
        'fup': PaddleCommand.FAST_UP,
        'fdown': PaddleCommand.FAST_DOWN
    }

    def connect(self):
        try:
            self.match_id = int(self.scope['url_route']['kwargs']['match_id'])
        except ValueError:
            self.close(400)
            return

        # Authentication
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            self.close(4001)
            return

        # Check requested role in url query string
        # Format: role=[spectator|challenger|host]
        try:
            query_data = urllib.parse.parse_qs(self.scope['query_string'],
                                               strict_parsing=True,
                                               max_num_fields=1
                                               )
        except ValueError:
            self.close(400)
            return

        try:
            requested_role = query_data[b'role'][0].decode('utf-8')
        except (KeyError, IndexError, UnicodeError):
            self.close(400)
            return

        if requested_role not in ('spectator', 'host', 'challenger'):
            self.close(400)
            return

        try:
            self.match = OngoingMatch.objects.get(pk=self.match_id)
        except OngoingMatch.DoesNotExist:
            self.close(404)
            return

        with transaction.atomic():
            try:
                if requested_role == 'spectator':
                    self.match.add_spectator(self.user)
                elif requested_role == 'host':
                    if self.user.pk != self.match.host.pk:
                        self.close(403)
                        return
                elif requested_role == 'challenger':
                    self.match.challenger = self.user
            except ValueError:
                self.close(400)
                return

            self.role = requested_role
            # Join match group
            self.match_group_name = f'game_{self.match_id}'

            async_to_sync(self.channel_layer.group_add)(
                self.match_group_name,
                self.channel_name
            )
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'role'):  # if a role has been created - that is, the consumer has at least came to set the user
            # The players remain in the game until the end of the game
            if self.role == 'spectator':
                self.match.remove_spectator(self.user)

            if self.role == 'challenger' and not self.match.is_started:
                self.match.remove_challenger()

        # Leave room group
        if hasattr(self, 'match_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.match_group_name,
                self.channel_name
            )

    def receive_json(self, content, **kwargs):
        print(content)
        if self.role == 'spectator':
            return

        try:
            command = content['command']
        except KeyError:
            self.send_json({'error': 'no command sent', 'code': GameConsumer.NO_COMMAND})
            return

        # before match starts
        if not self.match.is_started:
            if self.role == 'host':
                if command == 'start_match':
                    try:
                        self.match.start_match()

                        game_input = QueueInput(max_size=GameConsumer.MAX_INPUT_QUEUE_SIZE)
                        game_output = QueueOutput(max_size=GameConsumer.MAX_INPUT_QUEUE_SIZE)
                        PongOutputConsumer(game_output, self.channel_layer, self.match_group_name, self.match).start_consuming()
                        self.game = Controller(game_input, game_output)

                        games_to_input_handler[self.match.pk] = game_input
                    except IntegrityError:
                        self.send_json({'error': 'challenger not ready', 'code': GameConsumer.CHALLENGER_NOT_READY})
                else:
                    self.send_json({'error': 'invalid command', 'code': GameConsumer.INVALID_COMMAND})

            elif self.role == 'challenger':
                if command == 'ready':
                    self.match.set_challenger_ready()
                else:
                    self.send_json({'error': 'invalid command', 'code': GameConsumer.INVALID_COMMAND})
            return

        # match started
        elif command not in ('up', 'down', 'fup', 'fdown'):
            self.send_json({'error': 'invalid command', 'code': GameConsumer.INVALID_COMMAND})
            return

        input = games_to_input_handler[self.match.pk]
        if self.role == 'host':
            input.left_paddle_input = GameConsumer.COMMANDS[command]
        else:
            input.right_paddle_input = GameConsumer.COMMANDS[command]

    def game_update(self, message):
        self.send_json(message)

    def end_game(self, message):
        self.send_json(message)
        self.close(200)



