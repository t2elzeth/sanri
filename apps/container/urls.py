from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContainerAPIView.as_view()),
    path("<int:pk>/", views.ContainerDetailAPIView.as_view()),
]
