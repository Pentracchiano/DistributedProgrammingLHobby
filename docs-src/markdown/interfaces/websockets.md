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
  
##### The client is an host of a match but the match he wants to join is another one:

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

A challenger to communicate that it is ready to play must send the following command:

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

