In this section, the overall architecture of the actual game will be described, together with the reasons behind the
decisions that were taken.

## Game structure

### Hexagonal architecture
The game was developed from scratch because no implementation was found that was properly decoupled from the keyboard
and a display. In fact, the game needed to easily communicate with the client code using sockets, and also using the
keyboard for testing purposes.

The game architecture is therefore centered on this purpose: it heavily relies on the so-called *hexagonal architecture*
as described in [this article](https://www.viewfromthecodeface.com/portfolio/clean-code-hexagonal-architecture/) and on
the *dependency injection* pattern.

### Game files

These are the files implementing the game logic:

```
├── ball.py
├── controller.py
├── game_rules.py
└── paddle.py
```

## Game objects

### Ball and paddles

The game is object-oriented: `ball.py` and `paddle.py` implement the corresponding objects logic, exposing a `move()`
method which updates their state. The ball doesn't need particular inputs because it just implements its physics
relatively to the surrounding world, while the paddle takes a command input.

Both methods take a time interval that is used to correctly update the objects state according to the amount of time
elapsed since the last call. 

### Controller

The controller is the true center of the game: it uses constants and definitions in `game_rules.py` to determine global
game rules, and requires external `Input` and `Output` classes to work with. 

It is responsible for handling the ball and the paddles to implement the game. When initialized, it starts a new thread
in which the whole logic runs.

#### Input interface

The input class is used to take the paddles commands and process them: it needs to provide a `left_paddle_input` and a
`right_paddle_input` attributes asynchronously. The controller will use their current value during the game loop.
Must be thread-safe.

!!! question "Why attributes"
    While attributes may seem arbitrary and limiting some `Input` implementation choices, the `#!python @property` methods
    in Python work as attributes, removing this apparent limitation.

    Therefore, an implementer can create whatever logic they may feel fit, and the client will use the class cleanly.

    ```python
    current_command = input.left_paddle_input  # while an attribute, it can execute logic as a method if needed
    paddle.move(delta_t, current_command)
    ```

#### Output interface

The output class is used by the controller to communicate with the external clients at different times
during the execution of the game.
It needs to provide:

- a method `#!python init_game(data: dict)`, called only once at the very start of the game with configuration parameters 
  such as the width of the paddle, the length of the paddle, and the radius of the ball. It therefore signals that the game
  has started.
- a `#!python __call__(data: dict)` implementation which is called once every *server tick*, receiving game status data
  as a Python `#!python dict`. It contains information about the ball and paddles positions, whether the ball has just bounced,
  the current match time, and other relevant current information.
- a method `#!python end_game(data: dict)`, called only once to signal the final scores of the two players and
  the match time.
  
!!!tip 
    In order to avoid slowing down the game loop, it's best to implement the output class as a thread-safe *queue*
    which then gets read somewhere else.

### Actual input and output implementations

#### Local game

In order to test the game and the game only, an input-output implementation was created which used the keyboard presses
and the screen. It can be found in the package `game/pong/test/`, together with a `testing.py` module which can be
executed stand-alone to test the game locally. 

!!! example "Game controls"
    The local game supports two players: the left player should use:

    - ++w++ for moving the paddle upwards,
    - ++s++ for moving the paddle downwards,
    - ++left-shift++ for accelerating the paddle movements.
    
    While the right player should use:

    - ++arrow-up++ for moving the paddle upwards,
    - ++arrow-down++ for moving the paddle downwards,
    - ++right-shift++ for accelerating the paddle movements.

#### Queue-based 

In order to use the game from multiple threads correctly, an input-output implementation was created which makes use of
a custom `CircularQueue` class. This thread-safe queue is based on the `collections.deque` class,
can be configured to have a maximum size, after which old elements are replaced with new ones as they are inserted.
The queue uses the `wait/notify` pattern with *condition variables* in order to expose a blocking `get` method.

While the consumer of the `Input` queue is the controller itself and the producer is the websocket client,
it is now needed a consumer for dequeueing the items in the `Output` queue inserted by the controller game loop.
That is why the `game/pong_output_consumer.py` module was created. Its responsibility lies in dequeueing messages from
the `Output` and sending them at the Django Channels group of the corresponding match. Then, each websocket will send
to its client the message with the game status update.

The output queue inserts a `#!python "message_type"` key in the dictionary in order to propagate which of the
three methods created the `data` object which was put in the queue.
Here is a snippet which shows this behaviour:

```python linenums="1"
from game.pong.queue.circular_queue import CircularQueue


class QueueOutput:
    STATUS = 'status'
    INIT = 'init'
    END = 'end'

    def __init__(self, max_size: int):
        self.queue = CircularQueue(max_size)

    def __call__(self, game_status: dict):
        game_status_with_type = {'message_type': QueueOutput.STATUS}
        game_status_with_type.update(game_status)
        self.queue.put_nowait(game_status_with_type)

    def init(self, game_info: dict):
        game_info_with_type = {'message_type': QueueOutput.INIT}
        game_info_with_type.update(game_info)
        self.queue.put_nowait(game_info_with_type)

    def end_game(self, game_info: dict):
        game_info_with_type = {'message_type': QueueOutput.END}
        game_info_with_type.update(game_info)
        self.queue.put_nowait(game_info_with_type)
```

The whole implementation of this is found in `game/pong/queue/`.

!!!caution
    The size of the queues is an important parameter to set. Let's imagine that the server experiences a brief connection
    problem and, as a consequence, the output queue starts to accumulate items to be sent. It is important that the clients
    receive the most up-to-date status as possible to be able to play correctly: therefore, dropping *some* old packets
    will actually be beneficial to the clients, even if they experience a slight *jump* in their view of the game.

    If the queue is *too big*, this packet drop **never happens**, and the clients risk *living in the past* if problems arise.

    If the queue is *too small*, packets could be dropped when they could be easily sent in time.
