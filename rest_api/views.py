from django.http import Http404
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_api.models import *
from rest_api.serializers import *


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
        if ongoing:
            serializer = OngoingMatchSerializer(ongoing)
            return Response(serializer.data)
        raise Http404
