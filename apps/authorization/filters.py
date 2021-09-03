import django_filters


class BalanceFilter(django_filters.rest_framework.FilterSet):
    client = django_filters.CharFilter(
        field_name="client__id", lookup_expr="istartswith"
    )
    date_from = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte"
    )
    balance_action = django_filters.CharFilter(
        field_name="balance_action", lookup_expr="iexact"
    )
    payment_type = django_filters.CharFilter(
        field_name="payment_type", lookup_expr="iexact"
    )
