# REST API

## Overview

This section shows the list of all the resources available in the LHobby REST API.

## API Reference

### Create a new user

It allows to create a new user. You don't have to be authenticated to use this endpoint.

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

### List users

List all registered users. You must be authenticated to use this endpoint.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/users/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`Cookie`| string | header | session cookie for authentication| true if no Authorization |
|`Authorization`| string | header | token for authentication, it must be in this form: Token <token> | true if no Cookie | 

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

### User detail

Get detail of specific user using his `username`. You must be authenticated to use this endpoint.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/users/{username}/</code>
</pre>


#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`Cookie`| string | header | session cookie for authentication| true if no Authorization |
|`Authorization`| string | header | token for authentication, it must be in this form: Token <token> | true if no Cookie |
|`username`| string | path | user's username | true |

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

### User detailed ongoing match

Get the ongoing match of a specific user. You must be authenticated to use this endpoint.

<pre>
<code><span class="bg-blue text-white rounded-1 px-2 py-1" style="text-transform: uppercase">get</span> /HOST:PORT/api/users/{username}/ongoing_match/</code>
</pre>

#### Parameters

| Name | Type | In | Description | Required |
|-|-|-|-|-| 
|`Cookie`| string | header | session cookie for authentication| true if no Authorization |
|`Authorization`| string | header | token for authentication, it must be in this form: Token <token> | true if no Cookie |
|`username`| string | path | user's username | true |

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

### Login

Login into the system.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/login/</code>
</pre>

### Logout

Logout from the system. You must be authenticated to use this endpoint.

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

### Get authorization token

Use this endpoint to generate a token for the authentication.

<pre>
<code><span class="bg-indigo text-white rounded-1 px-2 py-1" style="text-transform: uppercase">post</span> /HOST:PORT/api/token/</code>
</pre>

#### Parameters

| Name    | Type | In | Description | Required |
|-|-|-|-|-| 
|`username`| string | body | the username of the user | true |
|`password`| string | body | the password of the user | true |

#### OK response

```
Status: 200 OK
```

```json

{
    "token": "b8a60e83569600e8f5c323428cca736ce9176e0f"
}

```

### Delete authorization token

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

### Ongoing matches



### Completed matches


