from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.AuthenticationViewSet, basename="authentication")

urlpatterns = router.urls
