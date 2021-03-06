# Rest API
In this section, interesting parts of the REST code will be explored and commented. 

## Models

!!!note
	Here, only code will be described: for the architecture, head to [the database reference](../architecture/index.md#Database).
### Operating on users in OngoingMatch
In the `rest_api_ongoingmatch` table, information about the currently playing users is not easily accessible. Furthermore, inserting and removing users consists of two operations, requiring both a change of role and of the `ongoing_match` foreign key of the user.

Rather than repeating often-used queries, Python's computed properties were used in order to simulate having hosts, challengers and spectators readily available and modifiable directly in the `#!python OngoingMatch` instance.
This helped to reduce the verbosity of the code, to respect the _Don't repeat yourself (DRY)_ principle and, more importantly, to avoid to forget to change both attributes in the user.

```python linenums="71"
@property
def host(self) -> typing.Optional[User]:
    try:
        return self.user_set.get(role=User.Role.HOST)
    except User.DoesNotExist:
        return None

@host.setter
def host(self, value: User):
    if self.host:
        raise ValueError('Host was already set')

    if value.ongoing_match:
        raise ValueError(f'User {value.username} is already in a match')

    value.ongoing_match = self
    value.role = User.Role.HOST
    value.save(update_fields=['role', 'ongoing_match'])
```

This snippet enables the use of simple syntax for accessing or setting the host of a match as if it were an attribute of the class:

```python
user = User.objects.get(username='msilla')
ongoing_match.host = user

print(ongoing_match.host)
>>> User(<msilla>)
```

The setter property also validates the inserting operation, raising `#!python ValueError` if incompatibilites arise.
Code equivalents exist for the challenger and spectator roles, with the only exception being the spectator methods permitting multiple players with the same role.

### Ending a match 
In order to complete a match correctly, it is needed to:

- update the players' ELOs;
- set the role and the `ongoing_match` of the players to `#!python None`;
- delete the current `OngoingMatch` instance from the database;
- create a corresponding `CompletedMatch` instance to keep track of the
games history.

It is very important to conduct all of these operations in a single database
 transaction, in order to avoid leaving the data in an inconsistent state — either for brief durations while *during* the execution, or until human intervention if any errors happen before completing the set of needed operations.

This is only one example of such a situation, which demonstrates the use
 of transactions in the Django Model API.

!!!important
     In the following snippet, the `ongoing_match` foreign key is not updated because it is automatically set to `#!sql NULL` by the DBMS due to the configured `on_delete` policy.

```python linenums="157"
def complete_match(self, winner: User, loser: User, winner_score: int, loser_score: int) -> CompletedMatch:
    users = [self.host, self.challenger]
    if winner.username == loser.username:
        raise ValueError('Winner and Loser must be different')
    if (winner not in users) or (loser not in users):
        raise ValueError('User not playing the game')

    new_winner_elo, new_loser_elo = compute_elos(winner, loser, winner_score, loser_score)

    with transaction.atomic():
        completed_match = CompletedMatch.objects.create(
            winner=winner,
            loser=loser,
            start_timestamp=self.start_timestamp,
            winner_score=winner_score,
            loser_score=loser_score,
            winner_elo_before_match=winner.elo,
            loser_elo_before_match=loser.elo,
            winner_elo_after_match=new_winner_elo,
            loser_elo_after_match=new_loser_elo
        )

        winner.elo = new_winner_elo
        loser.elo = new_loser_elo

        winner.role = None
        loser.role = None

        winner.save(update_fields=['elo', 'role'])
        loser.save(update_fields=['elo', 'role'])

        self.delete()

    return completed_match
```

## Views
While much of the views code is straightforward, there are interesting edge cases to take into account.

### OngoingMatch creation
When an `OngoingMatch` is created by a soon-to-be host via a `POST` request, it must also be linked to the user that started the request, in order to keep track of the ownership of the match.
Therefore, the match instance is created, and then the user must be updated by setting the new instance as the user's current match.

If the user is already in a game when making the request, or any unanticipated errors happen after having created the match, the database is left in an inconsistent state; a transaction is necessary to avoid this.

```python linenums="53"
def create(self, request, *args, **kwargs):
    with transaction.atomic():
        new_ongoing_match = OngoingMatch.objects.create()
        try:
            new_ongoing_match.host = request.user
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    serializer = OngoingMatchSerializer(instance=new_ongoing_match)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```
This code structure enforces a rollback of the database operations if any errors occur, while alerting the user. Otherwise, a normal `HTTP 201` response is returned together with the new object representation in the body, respecting REST design principles.

!!!success "Clean views"
	No substantial logic is therefore executed in the views, which only *glue together* other code: the error validation is done inside the model (just as described in [the previous section](#operating-on-users-in-ongoingmatch)), the serialization of the new instance to a Python `#!python dict` is handled by the serializer, and the JSON serialization is made by the `Response` internal handlers.

