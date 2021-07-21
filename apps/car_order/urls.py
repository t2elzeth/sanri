from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarOrderAPIView.as_view(), name="car-order-list-create"),
    path("Parking/", views.ParkingAPIView.as_view()),
    path("<int:pk>/", views.CarOrderDetailAPIView.as_view()),
]
