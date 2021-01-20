# Websockets

## Overview

This section shows the communication protocol between a client and the websocket server. The possible messages are related to the game phase and to
the `role` of the client in the match. The client must be __authenticated__ to communicate with the server.
 
## Protocol description

### Connection phase

First of all the client should start the communication with the server. In this phase the user must specify the role and the `id` of the match to join.

In order to start the communication, the client must open a websocket connection using the following url:


```
ws://HOST:PORT/ws/game/{match_id}/?role={role}
```

If the websocket request is not acceptable it maybe caused by server several errors.

#### Role independent errors

##### The match ID does not exist:

```json
{"error": "non existent requested match", "code": 5}
```

##### The user is not authenticated:

```json
{"error": "unauthenticated user, please send auth token", "code": 6}
```

##### The query string contains more than one parameter or is not well formed:

```json
{"error": "bad key in query string. expected: role", "code": 7}
```

##### The requested role is not in `[host, challenger, spectator]`:

```json
{"error": "bad value in query string. expected: [spectator, host, challenger]", "code": 7}
```

#### Challenger or spectator related error

##### The client requested to be a spectator or a challenger but the user is already in a match or the match is full:

```json
{"error": "trying to join a match while already in another match or the match is full", "code": 9}
```
  
#### Host related error
  
##### The client requested to be an host of a match different from the one already hosted:

```json
{"error": "trying to join a match as host which you did not start", "code": 8}
```

<hr>

##### Success

Finally, if everything is ok for the server, the connection is established, and the client receives:

```json
{"status": "success", "code": 0}
```

From now on the websocket server can receive different type of `commands` from its client. If the requested role is `spectator`, 
the websocket server will ignore all the command coming from that user. 

### Game initialization phase

After established the connection with the websocket server for a specific ongoing match, it is time to start the game.
The host of the match is responsible for starting the match. A match can start only if a challenger is present and is 
ready to play.

#### Role independent error

If a client sends a message without the `command` keyword, the websocket server will always answer as follow:

```json

{"error": "no command sent", "code": 2}

```  

#### Challenger ready

A challenger in order to communicate that is ready to play must send the following command:

```json

{"command": "ready"}

```

From this moment, until the match begins, all commands sent from the challenger will be ignored and the client will receive the following error:

```json

{"error": "invalid command", "code": 2}

```

#### Host start match

In order to start the match the host must send the following command:

```json

{"command": "start_match"}

```

This will [start the game](../code-description-and-examples/game.md#controller) thread if the challenger is ready, otherwise the host will receive an error as follow:

```json

{"error": "challenger not ready", "code": 3}

```

### Game phase

The game has started and now the pong game screen is built by the clients connected to the same match, taking into 
account the parameters inside the init message, such as:

```json

{
    "message_type": "init",

    "ball_radius": 0.02,
    "paddle_height": 0.13,
    "paddle_width": 0.02
}

```

![pong](/assets/pong-start.png)

During the match the host controls the left paddle and the challenger the right one. In order to play, users can send 
the following commands:

```json

{"command": "up"}

```

```json

{"command": "down"}

```

```json

{"command": "fup"}

```

```json 

{"command": "fdown"} 

```

During the game, for each `game_tick`, the websocket server sends the clients all the messages containing the information
necessary to update the game status.

```json

{
    "message_type": "status",

    "has_bounced": true,
    "left_paddle_margin_reached": false,
    "right_paddle_margin_reached": true,
    "left_score": 4,
    "right_score": 3,
    "left_paddle_y": 0.5,
    "right_paddle_y": 0.3,
    "ball_x": 0.6,
    "ball_y": 1,
    "match_time": 33,
    "sudden_death": false
}

```

When the match is over, the server sends all participants a end message. The information is contained in a 
serialized completed match object — the same that would be sent from the 
[completed match API](rest-api.md#completed-match-detail).

```json
{
    "message_type": "end",

    "id": 1,
    "winner": "davide",
    "loser": "emanuele",
    "start_timestamp": "2021-01-16T16:40:51.981401Z",
    "completion_timestamp": "2021-01-16T16:41:20.669025Z",
    "winner_score": 5,
    "loser_score": 4,
    "winner_elo_before_match": 1000,
    "loser_elo_before_match": 1000,
    "winner_elo_after_match": 1050,
    "loser_elo_after_match": 950
}
```