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

As mentioned earlier, 