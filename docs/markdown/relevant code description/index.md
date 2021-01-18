# Overview 

The code is organized in Python packages as in the directory tree below:


```
├── DistributedProgrammingLHobby
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs
│   ├── markdown
│   │   ├── ... (this documentation files)
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
