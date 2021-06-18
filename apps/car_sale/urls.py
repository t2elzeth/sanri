from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.CarSaleViewSet, basename='car-sale')

urlpatterns = router.urls
