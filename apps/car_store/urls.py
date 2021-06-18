from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.CarStoreViewSet, basename="car-store")

urlpatterns = router.urls
