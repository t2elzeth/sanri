from django.urls import path

from . import views

urlpatterns = [
    path("", views.ShopCarAPIView.as_view(), name='shop-list'),
    path("<int:pk>/", views.ShopCarDetailAPIView.as_view(), name='shop-detail')
]
