# Overview

Topics external to the course are described in this section.

## [Django](https://www.djangoproject.com/)

Django is a Python web framework aimed at providing much of the usual *boilerplate* code as built-in directly out of the box.

For what concerns this project, it provided easy management of a database through the 
Django [*Object Relational Mapping (ORM)*](https://docs.djangoproject.com/en/3.1/topics/db/models/), registration
of users, session management, multithreaded request handling. 

In particular, the ORM was extremely useful for easily modifying and accessing the database directly in Python,
abstracting the SQL tables as object-oriented classes: the Django models. 
It also made possible the version control of the different
database changes through the proper use of [migrations](https://docs.djangoproject.com/en/3.1/topics/migrations/); this
helped the collaborative process, especially by making sure everyone on the team had the same version of the database. 

The migrations also help decoupling the database schema from the actual DBMS being used - since they are Python code,
they are translated into the correct SQL dialect when the DBMS is configured, letting us not worry about which one to
choose early on: a simple one, SQLite, was chosen, and if it were to be changed (due to for example performance issues),
no problems would have arisen.

!!! note
    While learning to use this framework and related tools took a substantial chunk of time from the actual development,
    it ended up being a good investment: it speeded up the construction of the features we wanted to implement and avoided
    the *reinvention of the wheel*.

Usually, Django is used stand-alone only in order to build Web pages; what we did want was instead a REST API, in order
to be independent from the particular choice of client. So, the actual HTTP and Websocket requests were served by two
Django libraries which expand the framework capabilities.

### [Django REST framework](https://www.django-rest-framework.org/)

Django REST framework adapts Django normal operations to work with HTTP methods commonly used in REST APIs, such as
`DELETE`, providing with standard implementations — in this example, it would remove the requested resource.

This particular framework was chosen because well integrated with the Django ORM: resources are, if necessary,
able to be directly mapped to Django models.
Moreover, it exposes a Browsable API: if you navigate to a REST endpoint, you can use it seamlessly in a nice user interface
directly from the browser. This grants a nice client for the API and was also very useful during the development.

### [Websockets](https://tools.ietf.org/html/rfc6455)

The game itself is a real-time application. Building one with REST calls is not ideal, especially in the case of a game,
where the server sends information about its state periodically without the clients requesting. 

Therefore, a better-suited protocol was needed: Websockets were chosen because they are full-duplex, work well in real-time,
but primarily because they are based on an HTTP handshake. This means that browser clients are easily supported (support otherwise
not achievable using normal UDP or TCP sockets), and user authentication can be handled with the same means used in the REST API.

#### [Django Channels](https://channels.readthedocs.io/en/stable/)

Django does not support Websockets, but the same organization maintains Django Channels, an extension of the framework
which implements Websockets and other long-running protocols, such as MQTT. As REST framework, it has access to the Django ORM.

An important peculiarity of Channels is the *channel layer*, a system which allowed us to exchange messages between
the different Websocket handlers, the *consumers*. In particular, each Websocket connection of LHobby is linked to a *channel group*; 
whenever there is a message that is to be sent to all the participants of a match (such as a game update), the server
code sends it to the channel group. The channel layer then sends the message to each consumer, which handles it
by simply sending it to the corresponding Websocket. 
