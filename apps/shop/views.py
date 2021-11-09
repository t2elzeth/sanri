from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .dto.car import AddCarDTO
from .serializers import AddCarSerializer, GetCarSerializer
from .services.car import AddCarService


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
