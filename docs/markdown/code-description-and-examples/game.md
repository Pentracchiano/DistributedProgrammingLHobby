In this section, the overall architecture of the actual game will be described, together with the reasons behind the
decisions that were taken.

## Game structure

#### Hexagonal architecture
The game was developed from scratch because no implementation was found that was properly decoupled from the keyboard
and a display. In fact, the game needed to easily communicate with the client code using sockets, and also using the
keyboard for testing purposes.

The game architecture is therefore centered on this purpose: it heavily relies on the so-called *hexagonal architecture*
as described in [this article](https://www.viewfromthecodeface.com/portfolio/clean-code-hexagonal-architecture/) and on
the *dependency injection* pattern.

#### Game files

These are the files implementing the game logic:

```
├── ball.py
├── controller.py
├── game_rules.py
└── paddle.py
```

#### Ball and paddles

The game is object-oriented: `ball.py` and `paddle.py` implement the corresponding objects logic, exposing a `move()`
method which updates their state. The ball doesn't need particular inputs because it just implements its physics
relatively to the surrounding world, while the paddle takes a command input.

Both methods take a time interval that is used to correctly update the objects state according to the amount of time
elapsed since the last call. 

#### Controller

The controller is the true center of the game: it uses constants and definitions in `game_rules.py` to determine global
game rules, and requires external `Input` and `Output` classes to work with. 

##### Input interface

The input class is used to take the paddles commands and process them: 