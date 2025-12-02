from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("", RedirectView.as_view(url='/api/docs/', permanent=False)),
    # path("", include("apps.core.urls")),
    path("admin/", admin.site.urls), 
    path('api/v1/shop/', include('apps.shop.api.v1.urls')),
    path('api/v1/orders/', include('apps.orders.api.v1.urls')),
    path('api/v1/auth/', include('apps.users.api.v1.urls')),
    path('api/v1/admin/', include('apps.shopmaster.api.v1.urls')),
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]