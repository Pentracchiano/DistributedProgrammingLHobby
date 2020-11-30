from rest_framework import serializers
from rest_api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'date_joined', 'elo', 'ongoing_match', 'role']
        read_only_fields = ['date_joined', 'elo', 'ongoing_match', 'role']


class CompletedMatchSerializer(serializers.ModelSerializer):
    winner = serializers.CharField(source='winner.username', read_only=True)
    loser = serializers.CharField(source='loser.username', read_only=True)

    class Meta:
        model = CompletedMatch
        fields = '__all__'


class OngoingMatchSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    challenger = UserSerializer(read_only=True)
    spectators = UserSerializer(many=True, read_only=True)

    class Meta:
        model = OngoingMatch
        fields = ['id', 'host', 'spectators', 'challenger', 'creation_timestamp', 'start_timestamp', 'is_started',
                  'is_challenger_ready']
        read_only_fields = ['id', 'host', 'spectators', 'challenger', 'creation_timestamp', 'start_timestamp', 'is_started',
                            'is_challenger_ready']
