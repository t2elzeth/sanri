from django.urls import path

from . import views

urlpatterns = [
    path("", views.StatisticAPIView.as_view(), name='statistic')
]
