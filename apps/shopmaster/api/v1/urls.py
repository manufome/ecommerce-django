from django.urls import path
from .views import get_admin_overview, get_dummy_data

urlpatterns = [
    path('home/', get_admin_overview, name='get_admin_overview'),
    path('dummy-data/', get_dummy_data, name='get_dummy_data'),
]