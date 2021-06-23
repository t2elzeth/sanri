from django.urls import path

from . import views

urlpatterns = [
    path("", views.MonthlyPaymentAPIView.as_view()),
    path("<int:id>/", views.MonthlyPaymentDetailAPIView.as_view()),
    path("Type/", views.MonthlyPaymentTypeAPIView.as_view()),
    path("Type/<int:id>/", views.MonthlyPaymentTypeDetailAPIView.as_view()),
]
