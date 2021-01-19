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

- The match ID is not a number or is not present in the request:

    ```json
    {"type": "websocket.close", "code": 4000}
    ```

- The user is not authenticated:

    ```json
    {"type": "websocket.close", "code": 4001}
    ```

- The query string contains more than one parameter or is not well formed:

    ```json
    {"type": "websocket.close", "code": 4000}
    ```

- The requested role is not in `[host, challenger, spectator]`:

    ```json
    {"type": "websocket.close", "code": 4000}
    ```

- The client requested to be a spectator or a challenger but is already in a match:

    ```json
    {"type": "websocket.close", "code": 4000}
    ```
  
- The client is an host of a match but the match he wants to join is another one:

    ```json
    {"type": "websocket.close", "code": 4003}
    ```
  

Finally, if everything is ok for the server, the connection is established, and the client receives:

```json
    {"type": "websocket.accept"}
```

#### Host



#### Challenger


#### Spectator

 