import django_filters

from .models import CarModel


class CarModelFilter(django_filters.rest_framework.FilterSet):
    mark = django_filters.CharFilter(
        field_name="mark__id", lookup_expr="iexact"
    )

    class Meta:
        model = CarModel
        fields = ["mark"]
