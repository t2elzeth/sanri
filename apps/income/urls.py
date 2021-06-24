from django.urls import path

from . import views

urlpatterns = [
    path("", views.IncomeAPIView.as_view()),
    path("<int:pk>/", views.IncomeDetailAPIView.as_view()),
    path("Type/", views.IncomeAPIView.as_view()),
    path("Type/<int:pk>/", views.IncomeDetailAPIView.as_view()),
]
