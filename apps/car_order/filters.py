import django_filters


class CarModelFilter(django_filters.rest_framework.FilterSet):
    of_client = django_filters.CharFilter(
        field_name="client__id", lookup_expr="iexact"
    )
    by_mark = django_filters.CharFilter(field_name="carModel__mark__name")
    client = django_filters.CharFilter(field_name="client__fullName", lookup_expr="istartswith")
    mark = django_filters.CharFilter(field_name="carModel__mark__name", lookup_expr="istartswith")
    model = django_filters.CharFilter(field_name="carModel__name", lookup_expr="istartswith")
    vinNumber = django_filters.CharFilter(field_name="vinNumber", lookup_expr="istartswith")
    lotNumber = django_filters.CharFilter(field_name="lotNumber", lookup_expr="istartswith")
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
