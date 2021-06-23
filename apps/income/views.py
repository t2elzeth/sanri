from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import Income, IncomeType
from .serializers import IncomeSerializer, IncomeTypeSerializer


class IncomeAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class IncomeDetailAPIView(DetailAPIViewMixin):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class IncomeTypeAPIView(generics.ListCreateAPIView):
    queryset = IncomeType.objects.all()
    serializer_class = IncomeTypeSerializer


class IncomeTypeDetailAPIView(DetailAPIViewMixin):
    queryset = IncomeType.objects.all()
    serializer_class = IncomeTypeSerializer
