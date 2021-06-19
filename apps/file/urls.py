from django.urls import path

from . import views

urlpatterns = [
    path("", views.FileModelAPIView.as_view()),
    path("<int:id>/", views.FileModelDetailAPIView.as_view()),
]
