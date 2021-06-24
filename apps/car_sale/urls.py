from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarSaleAPIView.as_view()),
    path("<int:pk>/", views.CarSaleDetailAPIView.as_view()),
]
