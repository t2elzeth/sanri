from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarModelAPIView.as_view()),
    path("<int:id>/", views.CarModelDetailAPIView.as_view()),
]
