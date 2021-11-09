from django.urls import path

from . import views

urlpatterns = (path("add/", views.AddCarView.as_view(), name="shop-car-add"),)
