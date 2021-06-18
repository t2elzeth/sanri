from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.CarOrderViewSet, basename="car-order")

urlpatterns = router.urls
