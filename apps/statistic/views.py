from django.db.models import (
    Case,
    Count,
    DecimalField,
    F,
    Q,
    Subquery,
    Sum,
    Value,
    When,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.models import Balance
from car_order.models import CarOrder
from car_resale.models import CarResale
from car_sale.models import CarSale
from container.models import Container, ContainerCar
from income.models import Income
from monthly_payment.models import MonthlyPayment
from staff.models import StaffExpense


class DateFilters:
    def __init__(self, request: Request):
        self.from_date = request.query_params.get("from")
        self.to_date = request.query_params.get("to")


class StatisticAPIView(APIView):
    def get(self, request, *args, **kwargs):
        date_filters = DateFilters(request)

        created_at_from = Q()
        created_at_to = Q()
        date_from = Q()
        date_to = Q()

        if date_filters.from_date:
            created_at_from = Q(created_at__gte=date_filters.from_date)
            date_from = Q(date__gte=date_filters.from_date)

        if date_filters.to_date:
            created_at_to = Q(created_at__gte=date_filters.to_date)
            date_to = Q(date__lte=date_filters.to_date)

        # Количество купленных машин
        car_orders = CarOrder.objects.filter(
            created_at_from, created_at_to
        ).aggregate(count=Count(1), sum=Sum("total"))

        # Количество безналичных переводов
        cashless_payments = Balance.objects.filter(
            created_at_from,
            created_at_to,
            payment_type=Balance.PAYMENT_TYPE_CASHLESS,
            balance_action=Balance.BALANCE_ACTION_REPLENISHMENT,
        ).aggregate(count=Count(1), sum=Sum("sum_in_jpy"))

        # Количество отправленных контейнеров
        shipped_containers = (
            Container.objects.filter(
                created_at_from, created_at_to, status=Container.STATUS_SHIPPED
            )
            .annotate(
                total=Case(
                    When(
                        client__atWhatPrice="by_fact",
                        then=Sum("container_cars__car__total"),
                    ),
                    When(
                        client__atWhatPrice="by_fob",
                        then=Sum("container_cars__car__total_FOB"),
                    ),
                    When(
                        client__atWhatPrice="by_fob2",
                        then=Sum("container_cars__car__total_FOB2"),
                    ),
                    default=Value(0),
                ),
                auctionFeesTotal=Sum("container_cars__car__auctionFees"),
                transportationTotal=Sum(
                    Case(
                        When(
                            container_cars__car__transport__gt=6000,
                            then=F("container_cars__car__transport"),
                        ),
                        default=Value(0),
                    )
                ),
                price10Total=Sum(F("container_cars__car__price") * 0.1),
                recycleTotal=Sum("container_cars__car__recycle"),
                amountTotal=Sum("container_cars__car__amount"),
                fobTotal=Sum("container_cars__car__client__sizeFOB"),
                income=Case(
                    When(
                        client__atWhatPrice="by_fact",
                        then=F("total")
                        + F("commission")
                        + F("containerTransportation")
                        + F("packagingMaterials")
                        + F("wheel_recycling__sum")
                        - F("wheel_sales__sum"),
                    ),
                    When(
                        Q(client__atWhatPrice="by_fob")
                        | Q(client__atWhatPrice="by_fob2"),
                        then=F("price10Total")
                        + F("recycleTotal")
                        + F("amountTotal")
                        + F("fobTotal")
                        - F("loading")
                        - F("auctionFeesTotal")
                        - F("transportationTotal"),
                    ),
                    default=0,
                    output_field=DecimalField(
                        max_digits=100, decimal_places=2
                    ),
                ),
            )
            .aggregate(sum=Sum("income"), count=Count(1))
        )

        # Количество загруженных машин в контейнеры
        loaded_cars = ContainerCar.objects.filter(
            created_at_from, created_at_to
        ).aggregate(count=Count(1), sum=Sum("car__total"))

        # Количество проданных машин на аукционах
        sold_cars = CarSale.objects.filter(
            created_at_from, created_at_to, status=True
        ).aggregate(count=Count(1), sum=Sum("total"))

        # Количество перепроданных машин
        car_resale = CarResale.objects.filter(
            created_at_from, created_at_to
        ).aggregate(count=Count(1), sum=Sum("salePrice"))

        # Количество припаркованных машин на стоянках
        parked_cars = CarOrder.objects.exclude(
            id__in=Subquery(ContainerCar.objects.all().values("car__id"))
        ).aggregate(count=Count(1), sum=Sum("total"))

        # Количество всех доходов
        incomes = Income.objects.filter(
            created_at_from, created_at_to
        ).aggregate(count=Count(1), sum=Sum("amount"))

        monthly_payments = MonthlyPayment.objects.filter(
            date_from, date_to
        ).aggregate(sum=Sum("amount"), number=Count(1))

        staff_expenses = StaffExpense.objects.filter(
            date_from, date_to
        ).aggregate(sum=Sum("amount"), number=Count(1))

        # Data to return
        data = {
            "car_orders": {
                "number": car_orders["count"],
                "sum": car_orders["sum"],
            },
            "cashless_payments": {
                "number": (cashless_payments["count"]),
                "sum": (cashless_payments["sum"]),
            },
            "shipped_containers": {
                "number": (shipped_containers["count"]),
                "sum": (shipped_containers["sum"]),
            },
            "loaded_cars": {
                "number": (loaded_cars["count"]),
                "sum": (loaded_cars["sum"]),
            },
            "sold_cars": {
                "number": (sold_cars["count"]),
                "sum": (sold_cars["sum"]),
            },
            "car_resale": {
                "number": (car_resale["count"]),
                "sum": (car_resale["sum"]),
            },
            "parked_cars": {
                "number": (parked_cars["count"]),
                "sum": (parked_cars["sum"]),
            },
            "incomes": {
                "number": (incomes["count"]),
                "sum": (incomes["sum"]),
            },
            "outcomes": {
                "sum": monthly_payments["sum"] + staff_expenses["sum"],
                "number": monthly_payments["number"]
                + staff_expenses["number"],
            },
            "overall": {
                "sum": incomes["sum"]
                - (monthly_payments["sum"] + staff_expenses["sum"])
            },
        }
        return Response(data=data)
