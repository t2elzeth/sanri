from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.CarResaleViewSet, basename="car-resale")

urlpatterns = router.urls
