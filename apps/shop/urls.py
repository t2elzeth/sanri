from django.urls import path

from . import views

urlpatterns = [
    path("", views.ShopCarAPIView.as_view(), name="shop-list"),
    path(
        "for_approve/",
        views.ShopCarForApproveView.as_view(),
        name="shop-list-for-approve",
    ),
    path(
        "for_approve/<int:pk>/",
        views.ShopCarForApproveDetailAPIView.as_view(),
        name="shop-list-for-approve-detail",
    ),
    path(
        "<int:pk>/", views.ShopCarDetailAPIView.as_view(), name="shop-detail"
    ),
]
