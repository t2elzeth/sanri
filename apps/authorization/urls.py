from django.urls import path

from . import views

urlpatterns = [
    # Authentication
    path("Authenticate/register/", views.RegisterAPIView.as_view()),
    path("Authenticate/login/", views.LoginAPIView.as_view()),
    path("Authenticate/me/", views.GetMeAPIView.as_view()),
    # Client
    path("Client/", views.ClientListAPIView.as_view()),
    path("Client/<int:pk>/", views.ClientAPIView.as_view()),
    # Employee
    path("Employee/", views.EmployeeAPIView.as_view()),
    path("Manager/", views.ManagerAPIView.as_view()),
    path("Manager/<int:pk>/", views.ManagerDetailAPIView.as_view()),
    path("Employee/<int:pk>/", views.EmployeeDetailAPIView.as_view()),
    # Balance
    path("Balance/", views.BalanceListAPIView.as_view()),
    path("Balance/<int:pk>/", views.BalanceAPIView.as_view()),
]
