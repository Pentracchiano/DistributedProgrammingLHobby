from django.db.models import QuerySet
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

    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='won_matches', null=True)
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='lost_matches', null=True)
    start_timestamp = models.DateTimeField()
    completion_timestamp = models.DateTimeField(auto_now_add=True)


class OngoingMatch(models.Model):

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    start_timestamp = models.DateTimeField(null=True)
    is_started = models.BooleanField(default=False)
    is_challenger_ready = models.BooleanField(default=False)

    @property
    def host(self) -> User:
        return self.user_set.get(role=User.Role.HOST)

    @property
    def challenger(self) -> User:
        return self.user_set.get(role=User.Role.CHALLENGER)

    @property
    def spectators(self) -> QuerySet:
        return self.user_set.filter(role=User.Role.SPECTATOR)
