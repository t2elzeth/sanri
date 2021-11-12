from django.urls import path

from . import views

urlpatterns = (
    path("", views.ListCarsView.as_view(), name="shop-car-list"),
    path("<int:pk>/", views.DetailCarView.as_view(), name="shop-car-detail"),
    path("add/", views.AddCarView.as_view(), name="shop-car-add"),
    path("requests/add/", views.AddBuyRequestView.as_view(), name="shop-buy-request-add"),
    path("requests/", views.ListBuyRequestsView.as_view(), name="shop-buy-request-list"),
    path("requests/<int:pk>/approve/", views.ApproveBuyRequestView.as_view(), name="shop-buy-request-approve"),
    path("requests/<int:pk>/decline/", views.DeclineBuyRequestView.as_view(), name="shop-buy-request-decline"),
)
