from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Sanri Backend",
        default_version="v1",
        description="This is backend for Sanri",
        contact=openapi.Contact(url="https://telegram.me/t2elzeth"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/", include("authorization.urls")),
    path("api/Auction/", include("auction.urls")),
    path("api/", include("car_model.urls")),
    path("api/CarOrder/", include("car_order.urls")),
    path("api/CarResale/", include("car_resale.urls")),
    path("api/CarSale/", include("car_sale.urls")),
    path("api/CarStore/", include("car_store.urls")),
    path("api/Container/", include("container.urls")),
    path("api/File/", include("file.urls")),
    path("api/Income/", include("income.urls")),
    path("api/MonthlyPayment/", include("monthly_payment.urls")),
    path("api/Staff/", include("staff.urls")),
    path("api/TransportCompanies/", include("transport_companies.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
