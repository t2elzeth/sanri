from django.urls import path

from . import views

urlpatterns = [
    path("", views.FileModelAPIView.as_view()),
    path("<int:pk>/", views.FileModelDetailAPIView.as_view()),
]
