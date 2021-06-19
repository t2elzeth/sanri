from django.urls import path

from . import views

urlpatterns = [
    path("Authenticate/register/", views.RegisterAPIView.as_view()),
    path("Authenticate/login/", views.LoginAPIView.as_view()),
    path("Client/", views.ClientListAPIView.as_view()),
    path("Client/<int:id>/", views.ClientAPIView.as_view()),
]
