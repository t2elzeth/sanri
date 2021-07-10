from django.urls import path

from . import views

urlpatterns = [
    path("CarMark/", views.CarMarkListAPIView.as_view()),
    path("CarModel/", views.CarModelAPIView.as_view()),
    path("CarModel/<int:pk>/", views.CarModelDetailAPIView.as_view()),
]
