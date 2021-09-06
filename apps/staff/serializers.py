from rest_framework import serializers

from .models import StaffExpense, StaffExpenseType, StaffMember


class StaffExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffExpenseType
        fields = ["id", "name"]


class WriteStaffExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffExpense
        fields = [
            "id",
            "staff_member",
            "type",
            "date",
            "amount",
            "comment",
        ]


class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = [
            "id",
            "full_name",
            "visa",
            "position",
            "visa_expiration_date",
        ]


class ReadStaffExpenseSerializer(serializers.ModelSerializer):
    type = StaffExpenseTypeSerializer()
    staff_member = StaffMemberSerializer()

    class Meta:
        model = StaffExpense
        fields = ["id", "staff_member", "type", "date", "amount", "comment"]
