from rest_framework import generics

from utils.mixins import DetailAPIViewMixin

from .models import StaffExpense, StaffExpenseType, StaffMember
from .serializers import (
    WriteStaffExpenseSerializer,
    StaffExpenseTypeSerializer,
    StaffMemberSerializer,
    ReadStaffExpenseSerializer,
)


class StaffExpenseAPIView(generics.ListCreateAPIView):
    queryset = StaffExpense.objects.all()
    serializer_class = WriteStaffExpenseSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = WriteStaffExpenseSerializer
        else:
            self.serializer_class = ReadStaffExpenseSerializer

        return super().get_serializer_class()


class StaffExpenseDetailAPIView(DetailAPIViewMixin):
    queryset = StaffExpense.objects.all()
    serializer_class = ReadStaffExpenseSerializer

    def get_serializer_class(self):
        if self.request.method in ("UPDATE", "PATCH"):
            self.serializer_class = WriteStaffExpenseSerializer
        else:
            self.serializer_class = ReadStaffExpenseSerializer

        return super().get_serializer_class()


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
