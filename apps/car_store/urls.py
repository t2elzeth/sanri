from django.urls import path

from . import views

urlpatterns = [
    path("", views.CarStoreAPIView.as_view()),
    path("<int:pk>/", views.CarStoreDetailAPIView.as_view()),
]
