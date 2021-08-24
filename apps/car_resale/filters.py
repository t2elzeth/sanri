import django_filters


class CarResaleFilter(django_filters.rest_framework.FilterSet):
    mark = django_filters.CharFilter(
        field_name="carModel__mark__id", lookup_expr="iexact"
    )
    model = django_filters.CharFilter(
        field_name="carModel__id", lookup_expr="iexact"
    )
    date_from = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte"
    )
