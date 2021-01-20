# Overview

Topics external to the course are described in this section.

## [Django](https://www.djangoproject.com/)

Django is a Python web framework aimed at providing much of the usual *boilerplate* code as built-in directly out of the box.

For what concerns this project, it provided easy management of a database through the 
Django [*Object Relational Mapping (ORM)*](https://docs.djangoproject.com/en/3.1/topics/db/models/), registration
of users, session management, multithreaded request handling. 

In particular, the ORM was extremely useful for easily modifying and accessing the database directly in Python,
abstracting the SQL tables as object-oriented classes. 
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
to be independent from the particular client chosen. So, the actual HTTP and Websocket requests were served by two
Django libraries which expand the framework capabilities.

### [Django REST framework](https://www.django-rest-framework.org/)

Django REST framework is 

#### Token authentication

### [Django channels](https://channels.readthedocs.io/en/stable/)

#### Websockets
