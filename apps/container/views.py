from authorization.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utils.mixins import DetailAPIViewMixin

from .models import Container
from .serializers import ContainerSerializer
from django.db.models import (
    Case,
    When,
    Sum,
    Value,
    F,
    Subquery,
    DecimalField,
    Q,
)


class ContainerAPIView(generics.ListCreateAPIView):
    queryset = (
        Container.objects.all()
        .select_related("wheel_recycling", "wheel_sales")
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
                output_field=DecimalField(max_digits=100, decimal_places=2),
            ),
            overall=Case(
                When(
                    client__atWhatPrice="by_fob",
                    then=F("total") + F("loading"),
                ),
                When(
                    client__atWhatPrice="by_fob2",
                    then=F("total") + F("transportation"),
                ),
                default=Value(0),
            ),
        )
    )
    serializer_class = ContainerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(client=self.request.user)
        elif user_type in (
            User.USER_TYPE_SALES_MANAGER,
            User.USER_TYPE_YARD_MANAGER,
        ):
            new_managed = Subquery(
                self.request.user.managed_users_as_manager.all()
                .select_related("user")
                .only("user")
                .values("user")
            )
            new_queryset = self.queryset.filter(client__id__in=new_managed)
            self.queryset = new_queryset

        return super().get_queryset()


class ContainerDetailAPIView(DetailAPIViewMixin):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
