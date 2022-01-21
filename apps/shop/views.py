from authorization.models import User
from django.db.models import Subquery
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .dto.buy_request import (
    AddBuyRequestDTO,
    ApproveBuyRequestDTO,
    DeclineBuyRequestDTO,
)
from .dto.car import AddCarDTO
from .models import BuyRequest, Car
from .serializers import (
    AddBuyRequestSerializer,
    AddCarSerializer,
    ApproveBuyRequestSerializer,
    DeclineBuyRequestSerializer,
    GetBuyRequestSerializer,
    GetCarSerializer,
)
from .services.buy_request import (
    AddBuyRequestService,
    ApproveBuyRequestService,
    DeclineBuyRequestService,
)
from .services.car import AddCarService


class ListCarsView(generics.ListAPIView):
    serializer_class = GetCarSerializer
    queryset = Car.objects.all()


class DetailCarView(generics.RetrieveAPIView):
    serializer_class = GetCarSerializer
    queryset = Car.objects.all()


class AddCarView(APIView):
    def post(self, request):
        serializer = AddCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dto = AddCarDTO(**data)
        service = AddCarService(data=dto)

        car = service.execute()
        return_data = GetCarSerializer(instance=car).data

        return Response(return_data, status=status.HTTP_201_CREATED)


class AddBuyRequestView(APIView):
    def post(self, request):
        serializer = AddBuyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dto = AddBuyRequestDTO(**data, from_client_id=self.request.user.id)
        service = AddBuyRequestService(data=dto)

        request = service.execute()
        return_data = GetBuyRequestSerializer(instance=request).data

        return Response(return_data, status=status.HTTP_201_CREATED)


class ListBuyRequestsView(generics.ListAPIView):
    serializer_class = GetBuyRequestSerializer
    queryset = BuyRequest.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.user_type == User.USER_TYPE_CLIENT:
            self.queryset = self.queryset.filter(
                from_client__id=self.request.user.id
            )
        elif self.request.user.user_type in (
            User.USER_TYPE_YARD_MANAGER,
            User.USER_TYPE_SALES_MANAGER,
        ):
            new_managed = Subquery(
                self.request.user.managed_users_as_manager.all()
                .select_related("user")
                .only("user")
                .values("user")
            )
            new_queryset = self.queryset.filter(
                from_client__id__in=new_managed
            )
            self.queryset = new_queryset

        return super().get_queryset()


class ApproveBuyRequestView(APIView):
    def post(self, request, pk):
        serializer = ApproveBuyRequestSerializer(data={"request_id": pk})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dto = ApproveBuyRequestDTO(**data)
        service = ApproveBuyRequestService(data=dto)

        req = service.execute()
        return_data = GetBuyRequestSerializer(instance=req).data
        return Response(return_data, status=status.HTTP_201_CREATED)


class DeclineBuyRequestView(APIView):
    def post(self, request, pk):
        serializer = DeclineBuyRequestSerializer(data={"request_id": pk})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dto = DeclineBuyRequestDTO(**data)
        service = DeclineBuyRequestService(data=dto)

        req = service.execute()
        return_data = GetBuyRequestSerializer(instance=req).data
        return Response(return_data, status=status.HTTP_201_CREATED)
