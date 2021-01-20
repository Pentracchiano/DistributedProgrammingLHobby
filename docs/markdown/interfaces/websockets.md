# Websockets

## Overview

This section shows the communication protocol between a client and the websocket server. The possible messages are related to the game phase and to
the `role` of the client in the match. The client must be __authenticated__ to communicate with the server.
 
## Protocol description

### Initialization phase

First of all the client should start the communication with the server. In this phase the user must specify the role and the `id` of the match to join.

In order to start the communication, the client must open a websocket connection using the following url:


```
ws://HOST:PORT/ws/game/{match_id}/?role={role}
```

If the websocket request is not acceptable by the server, these are the possible error messages:

- The match ID does not exist:

    ```json
    {"error": "non existent requested match", "code": 5}
    ```

- The user is not authenticated:

    ```json
    {"error": "unauthenticated user, please send auth token", "code": 6}
    ```

- The query string contains more than one parameter or is not well formed:

    ```json
    {"error": "bad key in query string. expected: role", "code": 7}
    ```

- The requested role is not in `[host, challenger, spectator]`:

    ```json
    {"error": "bad value in query string. expected: [spectator, host, challenger]", "code": 7}
    ```

- The client requested to be a spectator or a challenger but the user is already in a match or the match is full:

    ```json
    {"error": "trying to join a match while already in another match or the match is full", "code": 9}
    ```
  
- The client is an host of a match but the match he wants to join is another one:

    ```json
    {"error": "trying to join a match as host which you did not start", "code": 8}
    ```
  

Finally, if everything is ok for the server, the connection is established, and the client receives:

```json
    {"status": "success", "code": 0}
```

#### Host



#### Challenger


#### Spectator

 