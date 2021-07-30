from authorization.models import Balance
from car_order.models import CarOrder
from car_resale.models import CarResale
from car_sale.models import CarSale
from container.models import Container, ContainerCar
from income.models import Income
from rest_framework.response import Response
from rest_framework.views import APIView


class StatisticAPIView(APIView):
    def get(self, request, *args, **kwargs):
        from_ = request.query_params.get("from")
        to_ = request.query_params.get("to")

        # Количество купленных машин
        car_orders = CarOrder.objects.all()
        if from_:
            car_orders = car_orders.filter(created_at__gte=from_)
        if to_:
            car_orders = car_orders.filter(created_at__lte=to_)

        car_orders_number = car_orders.count()
        car_orders_sum = sum(car_order.total for car_order in car_orders)

        # Количество безналичных переводов
        cashless_payments = Balance.objects.filter(
            payment_type=Balance.PAYMENT_TYPE_CASHLESS
        )
        if from_:
            cashless_payments = cashless_payments.filter(created_at__gte=from_)
        if to_:
            cashless_payments = cashless_payments.filter(created_at__lte=to_)
        cashless_payments_number = cashless_payments.count()
        cashless_payments_sum = sum(
            payment.sum_in_jpy for payment in cashless_payments
        )

        # Количество отправленных контейнеров
        shipped_containers = Container.objects.filter(
            status=Container.STATUS_SHIPPED
        )
        if from_:
            shipped_containers = shipped_containers.filter(
                created_at__gte=from_
            )
        if to_:
            shipped_containers = shipped_containers.filter(created_at__lte=to_)
        shipped_containers_number = shipped_containers.count()
        shipped_containers_sum = sum(
            container.totalAmount for container in shipped_containers
        )

        # Количество загруженных машин в контейнеры
        loaded_cars = ContainerCar.objects.all()
        if from_:
            loaded_cars = loaded_cars.filter(created_at__gte=from_)
        if to_:
            loaded_cars = loaded_cars.filter(created_at__lte=to_)
        loaded_cars_number = loaded_cars.count()
        loaded_cars_sum = sum(car.car.total for car in loaded_cars)

        # Количество проданных машин на аукционах
        sold_cars = CarSale.objects.filter(status=True)
        if from_:
            sold_cars = sold_cars.filter(created_at__gte=from_)
        if to_:
            sold_cars = sold_cars.filter(created_at__lte=to_)
        sold_cars_number = sold_cars.count()
        sold_cars_sum = sum(car.total for car in sold_cars)

        # Количество перепроданных машин
        car_resale = CarResale.objects.all()
        if from_:
            car_resale = car_resale.filter(created_at__gte=from_)
        if to_:
            car_resale = car_resale.filter(created_at__lte=to_)
        car_resale_number = car_resale.count()
        car_resale_sum = sum(car.salePrice for car in car_resale)

        # Количество припаркованных машин на стоянках
        loaded_cars = [
            el["car__id"]
            for el in ContainerCar.objects.all().values("car__id")
        ]
        parked_cars = CarOrder.objects.exclude(id__in=loaded_cars)
        parked_cars_number = parked_cars.count()
        parked_cars_sum = sum(car.total for car in parked_cars)

        # Количество всех доходов
        incomes = Income.objects.all()
        if from_:
            incomes = incomes.filter(created_at__gte=from_)
        if to_:
            incomes = incomes.filter(created_at__lte=to_)
        incomes_number = incomes.count()
        incomes_sum = sum(income.amount for income in incomes)

        # Data to return
        data = {
            "car_orders": {
                "number": car_orders_number,
                "sum": car_orders_sum,
            },
            "cashless_payments": {
                "number": cashless_payments_number,
                "sum": cashless_payments_sum,
            },
            "shipped_containers": {
                "number": shipped_containers_number,
                "sum": shipped_containers_sum,
            },
            "loaded_cars": {
                "number": loaded_cars_number,
                "sum": loaded_cars_sum,
            },
            "sold_cars": {
                "number": sold_cars_number,
                "sum": sold_cars_sum,
            },
            "car_resale": {
                "number": car_resale_number,
                "sum": car_resale_sum,
            },
            "parked_cars": {
                "number": parked_cars_number,
                "sum": parked_cars_sum,
            },
            "incomes": {
                "number": incomes_number,
                "sum": incomes_sum,
            },
        }
        return Response(data=data)
