from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import MonthlyPayment, MonthlyPaymentType
from .serializers import (
    WriteMonthlyPaymentSerializer,
    MonthlyPaymentTypeSerializer,
    ReadMonthlyPaymentSerializer,
)


class MonthlyPaymentAPIView(generics.ListCreateAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = WriteMonthlyPaymentSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = WriteMonthlyPaymentSerializer
        else:
            self.serializer_class = ReadMonthlyPaymentSerializer

        return super().get_serializer_class()


class MonthlyPaymentDetailAPIView(DetailAPIViewMixin):
    queryset = MonthlyPayment.objects.all()
    serializer_class = ReadMonthlyPaymentSerializer

    def get_serializer_class(self):
        if self.request.method in ("UPDATE", "PATCH"):
            self.serializer_class = WriteMonthlyPaymentSerializer

        return super(MonthlyPaymentDetailAPIView, self).get_serializer_class()


class MonthlyPaymentTypeAPIView(generics.ListCreateAPIView):
    queryset = MonthlyPaymentType.objects.all()
    serializer_class = MonthlyPaymentTypeSerializer


class MonthlyPaymentTypeDetailAPIView(DetailAPIViewMixin):
    queryset = MonthlyPaymentType.objects.all()
    serializer_class = MonthlyPaymentTypeSerializer
