from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_api.models import OngoingMatch, User
from rest_framework.filters import OrderingFilter


class OngoingMatchFilter(filters.FilterSet):
    min_elo = filters.NumberFilter(method='filter_min_elo')
    max_elo = filters.NumberFilter(method='filter_max_elo')
    is_full = filters.BooleanFilter(method='filter_is_full')

    def filter_min_elo(self, queryset: QuerySet, name, value):
        return queryset.filter(user__role=User.Role.HOST, user__elo__gte=value)

    def filter_max_elo(self, queryset: QuerySet, name, value):
        return queryset.filter(user__role=User.Role.HOST, user__elo__lte=value)

    def filter_is_full(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(user__role=User.Role.CHALLENGER)
        else:
            return queryset.exclude(user__role=User.Role.CHALLENGER)

    class Meta:
        model = OngoingMatch
        fields = ['min_elo', 'max_elo', 'is_started', 'is_full']


class OrderingOngoingMatchFilter(OrderingFilter):

    elo_lookup = {
        'host_elo': 'user__elo',
        '-host_elo': '-user__elo'
    }

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            for i, field in enumerate(ordering):
                if field in OrderingOngoingMatchFilter.elo_lookup:
                    ordering[i] = OrderingOngoingMatchFilter.elo_lookup[field]
                    queryset = queryset.filter(user__role=User.Role.HOST)

            return queryset.order_by(*ordering)

        return queryset
