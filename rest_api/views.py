from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from rest_api.models import *
from rest_api.serializers import *
from rest_api.filters import OngoingMatchFilter, OrderingOngoingMatchFilter


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['elo', 'username']

    # todo permission_classes = []

    @action(detail=True)
    def completed_matches(self, request, **kwargs):
        user = self.get_object()

        result = request.query_params.get('result')
        if result == 'won':
            matches = user.won_matches.all()
        elif result == 'lost':
            matches = user.lost_matches.all()
        else:
            matches = CompletedMatch.objects.filter(Q(winner=user) | Q(loser=user))

        serializer = CompletedMatchSerializer(matches, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def ongoing_match(self, request, **kwargs):
        user = self.get_object()

        ongoing = user.ongoing_match
        if not ongoing:
            raise NotFound

        serializer = OngoingMatchSerializer(ongoing)
        return Response(serializer.data)


class OngoingMatchViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = OngoingMatch.objects.all()
    serializer_class = OngoingMatchSerializer
    filter_backends = [DjangoFilterBackend, OrderingOngoingMatchFilter]
    ordering_fields = ['host_elo']
    filterset_class = OngoingMatchFilter

    def create(self, request, *args, **kwargs):
        new_ongoing_match = OngoingMatch()
        try:
            new_ongoing_match.host = request.user
        except ValueError as e:
            raise serializers.ValidationError(str(e))

        new_ongoing_match.save()
        serializer = OngoingMatchSerializer(instance=new_ongoing_match)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def host(self, request, **kwargs):
        ongoing_match = self.get_object()
        serializer = UserSerializer(ongoing_match.host)
        return Response(serializer.data)

    @action(detail=True)
    def challenger(self, request, **kwargs):
        ongoing_match = self.get_object()
        challenger = ongoing_match.challenger
        if not challenger:
            raise NotFound
        serializer = UserSerializer(ongoing_match.challenger)
        return Response(serializer.data)

    @action(detail=True)
    def spectators(self, request, **kwargs):
        ongoing_match = self.get_object()
        serializer = UserSerializer(ongoing_match.spectators, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.host != self.request.user:
            raise PermissionDenied('You have not the permission to delete this match, you are not the HOST')
        if instance.is_started:
            raise serializers.ValidationError('You can\'t delete this match because it is already started')
        instance.delete()


class CompletedMatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompletedMatch.objects.all()
    serializer_class = CompletedMatchSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]



