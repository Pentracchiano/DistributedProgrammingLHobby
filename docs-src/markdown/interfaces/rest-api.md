# REST API

## Overview

This section shows the list of all the resources available in the LHobby REST API. Some endpoints require authentication.

!!! important "Authentication"
    
    :octicons-lock-16:{: .lock } If you see this icon, the endpoint requires authentication.
    
    :octicons-unlock-16:{: .unlock } If you see this icon, the endpoint does not require authentication.


## Authentication

There are two ways to do an authenticated request.

- __Token__: if you have an [authentication token](#get-authorization-token) you can do an authenticated request using the header key `Authorization` with `Token <authentication token>` as value.
- __Cookie__: if you are using a browser you can authenticate via the `Cookie` header key.

### :octicons-unlock-16:{: .unlock } Cookie based login

Login into the system. This endpoint is better suited for browser clients.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/login/</code>
</pre>

#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`username`| string | body | | true |
|`password`| string | body | | true |
|`next`| string | param | the url you will be redirected to | false | 

#### OK response
```
Status: 302 Found
```

### :octicons-lock-16:{: .lock } Cookie based logout 

Logout from the system. This endpoint is better suited for browser clients.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/logout/</code>
</pre>

#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`Cookie`| string | header | session cookie for authentication| true |

#### OK response
```
Status: 200 OK
```

### :octicons-unlock-16:{: .unlock } Get authorization token

Use this endpoint to generate a token for the authentication.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/token/</code>
</pre>

#### Parameters

| Name    | Type | In | Description | Required |
|-|-|-|-|-| 
|`username`| string | body |  | true |
|`password`| string | body |  | true |

#### OK response

```
Status: 200 OK
```

```json

{
    "token": "b8a60e83569600e8f5c323428cca736ce9176e0f"
}

```

### :octicons-lock-16:{: .lock } Delete authorization token

Use this endpoint to delete a specific user token.

<pre>
<code><span class="bg-red text-white rounded-1 px-2 py-1" style="text-transform: uppercase">delete</span> /HOST:PORT/api/token/</code>
</pre>

#### Parameters

| Name    | Type | In | Description | Required |
|-|-|-|-|-| 
|`Authorization`| string | header | token for authentication, it must be in this form: Token <token> | true |


#### Response

```
Status: 204 No Content
```

## API Reference

### :octicons-unlock-16:{: .unlock } Create a new user

It allows to create a new user.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/users/sign_up/</code>
</pre>

#### Parameters

| Name    | Type | In | Description | Required |
|-|-|-|-|-| 
|`username`| string | body | the username of the user | true |
|`password`| string | body | the password must contain at least 8 characters and it must not be too similar to the username | true |
|`email`| string | body | user email | false |
|`first_name`| string | body | user first name | false |
|`last_name`| string | body | user last name | false |


#### Created response

```
Status: 201 Created 
```

```json
{
    "username": "marta",
    "date_joined": "2021-01-18T19:08:25.023237Z",
    "elo": 1000,
    "ongoing_match": null,
    "role": null,
    "first_name": "",
    "last_name": ""
}
```

### :octicons-lock-16:{: .lock } List users

List all registered users.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/users/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`ordering`| string | param | if equal to one in `[elo, -elo, username, -username]` the user list will be ordered | false |

#### OK response

```
Status: 200 OK 
```

```json

[
    {
        "username": "emanuele",
        "date_joined": "2021-01-15T23:17:32.966236Z",
        "elo": 900,
        "ongoing_match": 40,
        "role": "H",
        "first_name": "",
        "last_name": ""
    },
    {
        "username": "davide",
        "date_joined": "2021-01-15T23:18:11.368676Z",
        "elo": 1000,
        "ongoing_match": null,
        "role": null,
        "first_name": "",
        "last_name": ""
    },
    {
        "username": "marta",
        "date_joined": "2021-01-18T19:08:25.023237Z",
        "elo": 1000,
        "ongoing_match": null,
        "role": null,
        "first_name": "",
        "last_name": ""
    }
]
```

### :octicons-lock-16:{: .lock } User detail

Get detail of specific user using his `username`.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/users/{username}/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`username`| string | path |  | true |

#### OK response

```
Status: 200 OK
```

```json
{
    "username": "marta",
    "date_joined": "2021-01-18T19:08:25.023237Z",
    "elo": 1000,
    "ongoing_match": null,
    "role": null,
    "first_name": "",
    "last_name": ""
}
```

### :octicons-lock-16:{: .lock } Ongoing match of a specific user

Get the ongoing match of a specific user.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/users/{username}/ongoing_match/</code>
</pre>

#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`username`| string | path |  | true |

#### OK response

```
Status: 200 OK
```

```json
{
    "id": 40,
    "host": {
        "username": "emanuele",
        "date_joined": "2021-01-15T23:17:32.966236Z",
        "elo": 900,
        "ongoing_match": 40,
        "role": "H",
        "first_name": "",
        "last_name": ""
    },
    "spectators": [],
    "challenger": null,
    "creation_timestamp": "2021-01-18T18:34:09.576490Z",
    "start_timestamp": null,
    "is_started": false,
    "is_challenger_ready": false
}
```

### :octicons-lock-16:{: .lock } Create a new ongoing match

It allows to create a new match for the authenticated user, setting them as `host` of the match.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/ongoing_matches/</code>
</pre>

#### Created response

```
Status: 201 Created
```

```json

{
    "id": 41,
    "host": {
        "username": "marta",
        "date_joined": "2021-01-18T19:08:25.023237Z",
        "elo": 1000,
        "ongoing_match": 41,
        "role": "H",
        "first_name": "",
        "last_name": ""
    },
    "spectators": [],
    "challenger": null,
    "creation_timestamp": "2021-01-19T09:56:45.727233Z",
    "start_timestamp": null,
    "is_started": false,
    "is_challenger_ready": false
}

```

!!! warning
    The user must not be already playing or spectating another match, otherwise the following response will be returned:
    ```
    Status: 400 Bad Request 
    ```
    
    ```json
    [
        "User davide is already in a match"
    ]
    ```

### :octicons-lock-16:{: .lock } List ongoing matches

List all ongoing matches.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/ongoing_matches/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`ordering`| string | param | if equal to one in `[host_elo, -host_elo]` the ongoing match list will be ordered | false |
|`is_full`| bool | param | if true, only the matches that already have a challenger will be returned, otherwise the ones without a challenger | false |
|`max_elo`| number | param | if given, the ongoing matches hosted by an user with an elo greater than `max_elo` will not be returned | false |
|`min_elo`| number | param | if given the the ongoing matches hosted by an user with an elo less than `min_elo` will not be returned | false |


#### OK response

```
Status: 200 OK
```

```json

[
    {
        "id": 40,
        "host": {
            "username": "emanuele",
            "date_joined": "2021-01-15T23:17:32.966236Z",
            "elo": 900,
            "ongoing_match": 40,
            "role": "H",
            "first_name": "",
            "last_name": ""
        },
        "spectators": [],
        "challenger": null,
        "creation_timestamp": "2021-01-18T18:34:09.576490Z",
        "start_timestamp": null,
        "is_started": false,
        "is_challenger_ready": false
    },
    {
        "id": 41,
        "host": {
            "username": "marta",
            "date_joined": "2021-01-18T19:08:25.023237Z",
            "elo": 1000,
            "ongoing_match": 41,
            "role": "H",
            "first_name": "",
            "last_name": ""
        },
        "spectators": [],
        "challenger": {
            "username": "davide",
            "date_joined": "2021-01-15T23:18:11.368676Z",
            "elo": 1000,
            "ongoing_match": 41,
            "role": "C",
            "first_name": "",
            "last_name": ""
        },
        "creation_timestamp": "2021-01-19T09:56:45.727233Z",
        "start_timestamp": null,
        "is_started": false,
        "is_challenger_ready": false
    }
]

```

### :octicons-lock-16:{: .lock } Ongoing match detail

Get detail of a specific ongoing match using his `id`.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/ongoing_matches/{id}/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`id`| string | path | id number of the ongoing match | true |

#### OK response

```
Status: 200 OK
```

```json
{
"id": 41,
"host": {
    "username": "marta",
    "date_joined": "2021-01-18T19:08:25.023237Z",
    "elo": 1000,
    "ongoing_match": 41,
    "role": "H",
    "first_name": "",
    "last_name": ""
},
"spectators": [],
"challenger": {
    "username": "davide",
    "date_joined": "2021-01-15T23:18:11.368676Z",
    "elo": 1000,
    "ongoing_match": 41,
    "role": "C",
    "first_name": "",
    "last_name": ""
},
"creation_timestamp": "2021-01-19T09:56:45.727233Z",
"start_timestamp": null,
"is_started": false,
"is_challenger_ready": false
}
```

### :octicons-lock-16:{: .lock } Delete specific ongoing match

Delete a specific ongoing match given the match `id`. 

<pre>
<code><span class="bg-red text-white rounded-1 px-2 py-1" style="text-transform: uppercase">delete</span> /HOST:PORT/api/ongoing_matches/{id}/</code>
</pre>

!!! note
    An ongoing match can be deleted only from its host and only if it is not started yet.

#### Parameters

| Name    | Type | In | Description | Required |
|-|-|-|-|-| 
|`id`| string | path |  id number of the ongoing match to delete | true |


#### Response

```
Status: 204 No Content
```

### :octicons-lock-16:{: .lock } Ongoing match user detail

Get detail of the host, the challenger or the spectators of a specific match.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/ongoing_matches/{id}/{role}/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`id`| string | path | id number of the ongoing match | true |
|`role`| string | path | choose one in `[host, challenger, spectators]` | true | 

#### OK response

```
Status: 200 OK
```

```json
{
    "username": "davide",
    "date_joined": "2021-01-15T23:18:11.368676Z",
    "elo": 1000,
    "ongoing_match": 41,
    "role": "C",
    "first_name": "",
    "last_name": ""
}
```

### Creation of a completed match

Completed matches are only automatically generated after the end of an ongoing match.


### :octicons-lock-16:{: .lock } List completed matches

List all completed matches.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/completed_matches/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`ordering`| string | param | if equal to one in `[id, winner, loser, start_timestamp, end_timestamp, completion_timestamp, winner_score, loser_score, winner_elo_before_match, winner_elo_after_match, loser_elo_before_match, loser_elo_after_match]` the ongoing match list will be ordered. Put a ' - ' before the ordering type for descending order | false |
|`winner`| string | param | filter completed matches with a specific winner | false |
|`loser`| string | param | filter completed matches with a specific loser | false |
|`user`| string | param | filter completed matches with a specific user, it is not important if it is a winner or a loser | false |
|`end_timestamp_after`| datetime | param | the matches completed before the passed parameter will not be returned | false |
|`end_timestamp_before`| datetime | param | the matches completed after the passed parameter will not be returned  | false | 

!!! note
    `datetime` parameters must be formatted as: `yy:mm:dd` 

#### OK response

```
Status: 200 OK
```

```json

[
    {
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
]

```

### :octicons-lock-16:{: .lock } Completed match detail

Get detail of specific completed match using his `id`.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/completed_matches/{id}/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`id`| string | path | id number of the completed match | true |

#### OK response

```
Status: 200 OK
```

```json
{
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

The API REST can be used in order to create a new match or to visualize the available ongoing matches. To join a match
and play or spectate it clients shall use a websocket protocol. 

Next section will discuss such websocket protocol.