from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import StaffExpense, StaffExpenseType, StaffMember
from .serializers import (StaffExpenseSerializer, StaffExpenseTypeSerializer,
                          StaffMemberSerializer)


class StaffExpenseAPIView(generics.ListCreateAPIView):
    queryset = StaffExpense.objects.all()
    serializer_class = StaffExpenseSerializer


class StaffExpenseDetailAPIView(DetailAPIViewMixin):
    queryset = StaffExpense.objects.all()
    serializer_class = StaffExpenseSerializer


class StaffMemberAPIView(generics.ListCreateAPIView):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class StaffMemberDetailAPIView(DetailAPIViewMixin):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer


class StaffExpenseTypeAPIView(generics.ListCreateAPIView):
    queryset = StaffExpenseType.objects.all()
    serializer_class = StaffExpenseTypeSerializer


class StaffExpenseTypeDetailAPIView(DetailAPIViewMixin):
    queryset = StaffExpenseType.objects.all()
    serializer_class = StaffExpenseTypeSerializer
