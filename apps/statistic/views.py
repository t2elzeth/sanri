from authorization.models import Balance
from car_order.models import CarOrder
from car_resale.models import CarResale
from car_sale.models import CarSale
from container.models import Container, ContainerCar
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
from income.models import Income
from monthly_payment.models import MonthlyPayment
from rest_framework.response import Response
from rest_framework.views import APIView
from staff.models import StaffExpense


class DateFilters:
    def __init__(self, query):
        self.from_date = Q()
        self.to_date = Q()

        from_date = query.get("from")
        if from_date:
            self.from_date = Q(created_at__gte=from_date)

        to_date = query.get("to")
        if to_date:
            self.to_date = Q(created_at__lte=to_date)


class StatisticResult:
    def __init__(self, result: dict):
        self._sum = result["sum"]
        self._number = result["count"]

    @property
    def sum(self):
        return self._sum or 0

    @property
    def number(self):
        return self._number


class StatisticAPIView(APIView):
    def get(self, request, *args, **kwargs):
        date_filters = DateFilters(request.query_params)

        from_date = date_filters.from_date
        to_date = date_filters.to_date

        # Количество купленных машин
        car_orders = StatisticResult(
            CarOrder.objects.filter(from_date, to_date).aggregate(
                sum=Sum("total"), count=Count(1)
            )
        )

        # Количество безналичных переводов
        cashless_payments = StatisticResult(
            Balance.objects.filter(
                from_date,
                to_date,
                payment_type=Balance.PAYMENT_TYPE_CASHLESS,
                balance_action=Balance.BALANCE_ACTION_REPLENISHMENT,
            ).aggregate(sum=Sum("sum_in_jpy"), count=Count(1))
        )

        # Количество отправленных контейнеров
        shipped_containers = (
            Container.objects.filter(
                from_date, to_date, status=Container.STATUS_SHIPPED
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
        shipped_containers_result = StatisticResult(shipped_containers)

        # Количество загруженных машин в контейнеры
        loaded_cars = StatisticResult(
            ContainerCar.objects.filter(from_date, to_date).aggregate(
                count=Count(1), sum=Sum("car__total")
            )
        )

        # Количество проданных машин на аукционах
        sold_cars = StatisticResult(
            CarSale.objects.filter(from_date, to_date, status=True).aggregate(
                count=Count(1), sum=Sum("total")
            )
        )

        # Количество перепроданных машин
        car_resale = StatisticResult(
            CarResale.objects.filter(from_date, to_date).aggregate(
                count=Count(1), sum=Sum("salePrice")
            )
        )

        # Количество припаркованных машин на стоянках
        parked_cars = StatisticResult(
            CarOrder.objects.exclude(
                id__in=Subquery(ContainerCar.objects.all().values("car__id"))
            ).aggregate(count=Count(1), sum=Sum("total"))
        )

        # Количество всех доходов
        incomes = StatisticResult(
            Income.objects.filter(from_date, to_date).aggregate(
                count=Count(1), sum=Sum("amount")
            )
        )

        monthly_payments = StatisticResult(
            MonthlyPayment.objects.filter(from_date, to_date).aggregate(
                sum=Sum("amount"), count=Count(1)
            )
        )

        staff_expenses = StatisticResult(
            StaffExpense.objects.filter(from_date, to_date).aggregate(
                sum=Sum("amount"), count=Count(1)
            )
        )

        # Data to return
        data = {
            "car_orders": {
                "number": car_orders.number,
                "sum": car_orders.sum,
            },
            "cashless_payments": {
                "number": cashless_payments.number,
                "sum": cashless_payments.sum,
            },
            "shipped_containers": {
                "number": shipped_containers_result.number,
                "sum": shipped_containers_result.sum,
            },
            "loaded_cars": {
                "number": loaded_cars.number,
                "sum": loaded_cars.sum,
            },
            "sold_cars": {
                "number": sold_cars.number,
                "sum": sold_cars.sum,
            },
            "car_resale": {
                "number": car_resale.number,
                "sum": car_resale.sum,
            },
            "parked_cars": {
                "number": parked_cars.number,
                "sum": parked_cars.sum,
            },
            "incomes": {
                "number": incomes.number,
                "sum": incomes.sum,
            },
            "outcomes": {
                "sum": monthly_payments.sum + staff_expenses.sum,
                "number": monthly_payments.number + staff_expenses.number,
            },
            "overall": {
                "sum": incomes.sum
                - (monthly_payments.sum + staff_expenses.sum)
            },
        }
        return Response(data=data)
