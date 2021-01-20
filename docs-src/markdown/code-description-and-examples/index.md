The code is organized in Python packages as below. 
The highlighted packages are the most interesting packages - that is, containing
most of the logic of the project.

!!! abstract "Directory tree"
    ```hl_lines="12 34 44"
    ├── DistributedProgrammingLHobby
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── docs-src
    │   ├── markdown
    │   │   ├── ... (these documentation files as markdown sources)
    ├── docs
    │   └── ... (these HTML files)
    ├── game
    │   ├── authentication
    │   │   └── token.py
    │   ├── pong
    │   │   ├── queue
    │   │   │   ├── circular_queue.py
    │   │   │   ├── input.py
    │   │   │   └── output.py
    │   │   ├── test
    │   │   │   ├── input.py
    │   │   │   ├── output.py
    │   │   │   ├── requirements.txt
    │   │   │   └── testing.py
    │   │   ├── ball.py
    │   │   ├── controller.py
    │   │   ├── game_rules.py
    │   │   └── paddle.py
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── consumers.py
    │   ├── pong_output_consumer.py
    │   └── routing.py
    ├── rest_api
    │   ├── migrations
    │   │   ├── ... (database migration files)
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── views.py
    ├── client
    │   ├── pygame_client.py
    │   ├── requirements.txt
    │   └── retro.ttf
    ├── db.sqlite3
    ├── manage.py
    └── requirements.txt
    ```

## Packages description
**`DistributedProgrammingLHobby`** is the Django _site_ directory, containing global settings
for the whole **server** application. In particular, here it is defined:

- the HTTP handler (the `rest_api` package),
- the Websockets handler (the `game` package),
- the DBMS (SQLite3),
- the Django Channels *channel_layer* (a local Redis instance — a powerful engine was required for the game to be 
correctly handled in real-time with multiple connected users),
- supported authentication methods (token-auth aimed at stand-alone clients and cookie-based aimed at browser clients).

**`docs`** is the package containing the Markdown files and the custom styles of this documentation, 
built with the Mkdocs static-site engine.

**`game`** is responsible for handling the Websocket protocol requests, running the actual games 
using the code in the `pong` module, updating clients on the state of the game, and changing the
database according to the match results.

**`rest_api`** implements the API of the server from the ground up: it defines the SQL tables as 
a series of Django models and exposes them RESTfully.

**`client`** is a simple implementation of a client which interacts with both the API and the
Websocket server to demonstrate a typical user session on the LHobby platform. 

!!! info
    The provided program is a command-line client which **does not implement** all the possible actions a user may actually take
    using the server directly with a REST client. 

    It is therefore only intended to show the core functionality of the project, while much more could
    be achieved with a more complex client.

In the next sections, interesting project parts will be explored more deeply.
