from rest_framework.views import APIView
from rest_framework.response import Response


class ShopView(APIView):
    def post(self):
        return Response({"message": "OK!"})
