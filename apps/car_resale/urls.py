from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarResaleAPIView.as_view()),
    path("<int:id>/", views.CarResaleDetailAPIView.as_view()),
]
