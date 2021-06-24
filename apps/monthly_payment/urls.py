from django.urls import path

from . import views

urlpatterns = [
    path("", views.MonthlyPaymentAPIView.as_view()),
    path("<int:pk>/", views.MonthlyPaymentDetailAPIView.as_view()),
    path("Type/", views.MonthlyPaymentTypeAPIView.as_view()),
    path("Type/<int:pk>/", views.MonthlyPaymentTypeDetailAPIView.as_view()),
]
