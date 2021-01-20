# Usage

## Server

The server is built starting from the [Django](../external-dependencies/index.md#django) development server, a lightweight Web server written purely in Python. It has been
used in order to test and develop things rapidly without having to deal with configuring a production server – such as Apache. So, in order to start the server, you have to 
launch the following django command:

```bash

python3 manage.py runserver

```

This command starts the development server on `localhost` at port 8000. It is also possible to choose the port:

```bash

python3 manage.py runserver 8080

```

It is now possible to navigate the REST API and send requests to the server. To check all the available endpoints and
how to use them refer to the [REST API Reference](../interfaces/rest-api.md).

For example you can start [creating a new user](../interfaces/rest-api.md#create-a-new-user):

```

POST http://127.0.0.1:8000/api/users/sign_up/

``` 

In the request body you can simply pass:

```json
{
"username": "cool-username",
"password": "strong-password"
}
```

## Client

A simple Python client has been developed to test the REST API server and the Websocket server. It assumes that
you're running the server at port 8000.

Launch the client with the following command:

=== "Windows"
    
    ```
    
    python3 client\pygame_client.py
    
    ```


=== "Linux/macOS"

    ```bash
    
    python3 client/pygame_client.py
    
    ```

The client allows you to login into the system, create or join a match and play against other users. Obviously you can
execute two or more instances of the client to simulate more user connected to the system.

Once you are in a match, and the pong screen is shown, you can play the game using the following keyboard commands:

!!! example "Game controls"

    - ++w++ for moving the paddle upwards,
    - ++s++ for moving the paddle downwards,
    - ++left-shift++ for accelerating the paddle movements.
    
Enjoy your game! :)