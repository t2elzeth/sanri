from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.AuctionViewSet, basename='auction')

urlpatterns = router.urls
