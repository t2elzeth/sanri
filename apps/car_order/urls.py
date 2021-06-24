from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarOrderAPIView.as_view()),
    path("<int:pk>/", views.CarOrderDetailAPIView.as_view()),
]
