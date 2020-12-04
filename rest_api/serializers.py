from django.core import exceptions
from rest_framework import serializers
from rest_api.models import *
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = dict()
        try:
            # validate the password and catch the exception
            password_validation.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    class Meta:
        model = User
        fields = ['username', 'date_joined', 'elo', 'ongoing_match', 'role', 'first_name', 'last_name', 'email',
                  'password']
        read_only_fields = ['date_joined', 'elo', 'ongoing_match', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True}
        }


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
