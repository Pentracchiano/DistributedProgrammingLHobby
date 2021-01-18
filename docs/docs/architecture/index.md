# Overview

Qualcosa ad alto livello tipo sul fatto che è client-server usa le socket ecc

## Diagram

The following diagram provides an abstract overall outline of the entities in the system and the relationship between 
them.

![Diagramma](wip)

## Database 

The system's server makes use of a database in order to keep track of the information required for the correct 
functioning of the platform.

The different kind of information are stored in separate SQL tables, which are: 

* `rest_api_user` -  Stores different information about the users.
* `rest_api_ongoingmatch` - Stores information about ongoing matches.
* `rest_api_completedmatch` - Stores information about completed matches.
* `authtoken_token` - Token 

### Users

The system stores the following login information in order to let them register to the platform and keep track of their 
progress. 

* `username` - Unique username associated to the player required to log in.
* `password` - Password established at registration time, required to log in. Passwords are hashed using PBKDF2 as to 
               preserve the privacy of the users.
* `email` - E-mail address associated to the account.

Apart from the login data, other information concerning the gaming state of the user is stored, such as: 

* `ongoing_match_id` - Containing the unique identifier of the match in which the user is participating, if playing, 
                       otherwise _`<null>`_.
* `role` - Containing information about the role of the player, if associated to an ongoing match. The different possible 
roles are:   _host_, _challenger_, _spectator_.

Fields carrying other generic information about the user are:

* `elo` - Rating score indicating the skill level of the player.
* `date_joined` - Date and time of the registration of the user.
* `last_login` - Date and time of the last log in of the user.

Here follows an example of the _rest_api_user_ dataset table.

| __id__ | password | last_login | username | email | date_joined | role | ongoing_match_id | elo |
| -------| ----------- | ------------ | ------------ | --------- | --------------- | -------- | -------------------- | ------- |
| 1 | pbkdf2_sha256$...| 2021-01-18 18:00:00 |  davide | d.cafaro4@studenti.unisa.it | 2021-01-18 | H | 3 | 1000 | 
| 2 | pbkdf2_sha256$... | 2021-01-18 18:00:00 |emanuele| e.darminio4@studenti.unisa.it | 2021-01-18 | C | 3 | 1000 | 
| 3 | pbkdf2_sha256$... | 2021-01-18 18:00:00 | marta | m.silla@studenti.unisa.it | 2021-01-18 | S | 3 | 1000 |

#### Contraints

### Ongoing matches

To correctly link the players and spectators to the same match and synchronize their gaming status, each user keeps a 
reference to the relative ongoing match. The list of ongoing matches is stored in the dataset.

Each entry contains the following fields:

* `id` - Unique identifier of the match.
* `creation_timestamp` - Date and time of the creation of the match by the host.
* `start_timestamp` - Date and time of the start of the match.
* `is_started` - Boolean value used to know whether the game has started.
* `is_challenger_ready` - Boolean value used to alert the host that the challenger is ready. 

Here follows an example of the _rest_api_ongoing_matches_ dataset table.

| __id__ | creation_timestamp | start_timestamp | is_started | is_challenger_ready |
| -------| ----------- | ------------ | ------------ | --------- | 
| 3 | 2021-01-18 18:48:00 | 2021-01-18 18:50:00 |  1 | 1 |  

#### Contraints

### Completed matches 

When a match is completed the system stores the players scores and elos in order to keep track of their progress and 
allow competition.

| __id__ | start_timestamp      | completion_timestamp | loser_id | winner_id | loser_elo_after_match | loser_elo_before_match | loser_score | winner_elo_after_match | winner_elo_before_match | winner_score |
| -------| -------------------- | ------------ | ------------ | --------- | ---- | --- | --- | --- | --- | --- | 
| 1 | 2021-01-18 18:18:00 | 2021-01-18 18:30:00 |  1 | 2 |  950 | 1000 | 4 | 1050 | 1000 | 5 |
| 2 | 2021-01-18 18:28:00 | 2021-01-18 18:40:00 | 2 | 1 | 1000 | 1050 | 4 | 950 | 1000 | 5 |

#### Contraints



### Tokens

The token based authentication provided by the Django REST framework is used to allow users to verify their identity  
After the registration of a new user, the login function returns the token associated with the user. This token is then 
used to access the authenticated API.

In order to verify the identity of the user, tokens are stored in a SQL table and associated with the corresponding 
user ID as follows:

| key | created | user_id | 
| --- | ------- | ------- |
|fd726egydgnf75g...| 2021-01-18 18:00:00 | 1 |
|9h87ydb8ag8hjg6...| 2021-01-18 18:00:00 | 2 |
|uhdsa8dadh1hgf5...| 2021-01-18 18:00:00 | 3 |
 

## Server




## Client

