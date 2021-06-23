from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import MonthlyPayment, MonthlyPaymentType
from .serializers import MonthlyPaymentSerializer, MonthlyPaymentTypeSerializer


class MonthlyPaymentAPIView(generics.ListCreateAPIView):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer


class MonthlyPaymentDetailAPIView(DetailAPIViewMixin):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer


class MonthlyPaymentTypeAPIView(generics.ListCreateAPIView):
    queryset = MonthlyPaymentType.objects.all()
    serializer_class = MonthlyPaymentTypeSerializer


class MonthlyPaymentTypeDetailAPIView(DetailAPIViewMixin):
    queryset = MonthlyPaymentType.objects.all()
    serializer_class = MonthlyPaymentTypeSerializer
