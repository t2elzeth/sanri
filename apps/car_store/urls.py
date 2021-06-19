from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarStoreAPIView.as_view()),
    path("<int:id>/", views.CarStoreDetailAPIView.as_view()),
]
