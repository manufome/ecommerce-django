from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("", include("apps.core.urls")),
    path("admin/", admin.site.urls), 
    path('api/v1/shop/', include('apps.shop.api.v1.urls')),
    path('api/v1/orders/', include('apps.orders.api.v1.urls')),
    path('api/v1/auth/', include('apps.users.api.v1.urls')),
]