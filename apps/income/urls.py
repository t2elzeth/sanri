from django.urls import path

from . import views

urlpatterns = [
    path("", views.IncomeAPIView.as_view()),
    path("<int:id>/", views.IncomeDetailAPIView.as_view()),
    path("Type/", views.IncomeAPIView.as_view()),
    path("Type/<int:id>/", views.IncomeDetailAPIView.as_view()),
]