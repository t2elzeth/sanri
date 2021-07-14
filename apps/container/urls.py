from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContainerAPIView.as_view(), name="container-list-create"),
    path("<int:pk>/", views.ContainerDetailAPIView.as_view()),
]
