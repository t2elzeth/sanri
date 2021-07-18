from django.urls import path

from . import views

urlpatterns = [
    path("", views.TransportCompanyAPIView.as_view()),
    path("<int:pk>/", views.TransportCompanyDetailAPIView.as_view()),
]
