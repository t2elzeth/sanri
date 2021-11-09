from django.urls import path

from . import views

urlpatterns = (
    path("add/", views.AddCarView.as_view(), name="shop-car-add"),
    path("", views.ListCarsView.as_view(), name="shop-car-list"),
    path("requests/add/", views.AddBuyRequestView.as_view(), name="shop-buy-request-add"),
    path("requests/", views.ListBuyRequestsView.as_view(), name="shop-buy-request-list"),
)
