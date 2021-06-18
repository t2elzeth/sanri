from django.urls import path

from . import views

urlpatterns = [
    path('', views.ClientListAPIView.as_view()),
    path('<int:id>/', views.ClientAPIView.as_view()),
]
