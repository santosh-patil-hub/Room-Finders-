# urls.py

from django.urls import path
from .views import RegisterView, LoginView, TenantDashboardView, OwnerRoomView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tenant/dashboard/', TenantDashboardView.as_view(), name='tenant_dashboard'),
    path('owner/dashboard/', OwnerRoomView.as_view(), name='owner_dashboard'),
    path('owner/dashboard/<int:room_id>/', OwnerRoomView.as_view(), name='owner_dashboard_update'),  # for PUT method
]
