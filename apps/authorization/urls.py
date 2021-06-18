from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.AuthenticationViewSet)

urlpatterns = router.urls
