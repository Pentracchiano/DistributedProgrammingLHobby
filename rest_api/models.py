import typing

from django.db.models import QuerySet, Q, F
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        HOST = 'H', _('Host')
        CHALLENGER = 'C', _('Challenger')
        SPECTATOR = 'S', _('Spectator')

    elo = models.PositiveSmallIntegerField(default=1000)
    ongoing_match = models.ForeignKey('OngoingMatch', on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=1, choices=Role.choices, null=True)


class CompletedMatch(models.Model):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='won_matches',
                               null=True)
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='lost_matches',
                              null=True)
    start_timestamp = models.DateTimeField()
    completion_timestamp = models.DateTimeField(auto_now_add=True)

    winner_score = models.PositiveSmallIntegerField()
    loser_score = models.PositiveSmallIntegerField()
    winner_elo_before_match = models.PositiveSmallIntegerField()
    loser_elo_before_match = models.PositiveSmallIntegerField()
    winner_elo_after_match = models.PositiveSmallIntegerField()
    loser_elo_after_match = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(winner_score__gt=F('loser_score')),
                                   name='check_scores'),
            models.CheckConstraint(check=Q(winner_elo_before_match__lte=F('winner_elo_after_match')),
                                   name='check_winner_elo'),
            models.CheckConstraint(check=Q(loser_elo_before_match__gte=F('loser_elo_after_match')),
                                   name='check_loser_elo'),
            models.CheckConstraint(check=Q(completion_timestamp__gt=F('start_timestamp')),
                                   name='check_timestamp'),
            models.CheckConstraint(check=~Q(winner=F('loser')),
                                   name='check_cant_play_alone')
        ]


class OngoingMatch(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    start_timestamp = models.DateTimeField(null=True)
    is_started = models.BooleanField(default=False)
    is_challenger_ready = models.BooleanField(default=False)

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
        value.save()

    @property
    def challenger(self) -> typing.Optional[User]:
        try:
            return self.user_set.get(role=User.Role.CHALLENGER)
        except User.DoesNotExist:
            return None

    @challenger.setter
    def challenger(self, value: User):
        if self.challenger:
            raise ValueError('Challenger was already set')

        if value.ongoing_match:
            raise ValueError(f'User {value.username} is already in a match')

        value.ongoing_match = self
        value.role = User.Role.CHALLENGER
        value.save()

    @property
    def spectators(self) -> QuerySet:
        return self.user_set.filter(role=User.Role.SPECTATOR)

    def add_spectator(self, value: User):
        if value.ongoing_match:
            raise ValueError(f'User {value.username} is already in a match')

        value.ongoing_match = self
        value.role = User.Role.SPECTATOR
        value.save()

    class Meta:
        constraints = [
            models.CheckConstraint(check=(Q(is_started=True) & Q(is_challenger_ready=True))
                                         | (Q(is_started=False) & Q(is_challenger_ready=False))
                                         | (Q(is_started=False) & Q(is_challenger_ready=True)), name='check_state')
        ]
