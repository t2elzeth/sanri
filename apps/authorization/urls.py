from django.urls import path

from . import views

urlpatterns = [
    # Authentication
    path("Authenticate/register/", views.RegisterAPIView.as_view()),
    path("Authenticate/login/", views.LoginAPIView.as_view()),
    # Client
    path("Client/", views.ClientListAPIView.as_view()),
    path("Client/<int:id>/", views.ClientAPIView.as_view()),
    # Employee
    path("Employee/", views.EmployeeAPIView.as_view()),
    path("Employee/<int:id>/", views.EmployeeDetailAPIView.as_view()),
]
