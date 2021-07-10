import django_filters

from .models import CarOrder


class CarModelFilter(django_filters.rest_framework.FilterSet):
    of_client = django_filters.CharFilter(field_name='client__id', lookup_expr="iexact")

    class Meta:
        model = CarOrder
        fields = ["of_client"]
