from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarResaleAPIView.as_view(), name="car-resale-list-create"),
    path(
        "<int:pk>/",
        views.CarResaleDetailAPIView.as_view(),
        name="car-resale-detail",
    ),
]
