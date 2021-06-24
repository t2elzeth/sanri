from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionAPIView.as_view()),
    path("<int:pk>/", views.AuctionDetailAPIView.as_view()),
]
