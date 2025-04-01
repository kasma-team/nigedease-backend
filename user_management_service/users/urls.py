from django.urls import path
from .views import (
    UserListView, UserDetailView,
    RoleListView, RoleDetailView,
    PermissionListView, PermissionDetailView,
    ActivityLogView, ActivityLogDetailView
)
from .views.auth import LoginView, VerifyOTPView, ResendOTPView, RefreshTokenView, VerifyTokenView

urlpatterns = [
    # User management endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:id>/', UserDetailView.as_view(), name='user-detail'),
    
    # Role management endpoints
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<str:id>/', RoleDetailView.as_view(), name='role-detail'),
    
    # Permission management endpoints
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
    path('permissions/<str:id>/', PermissionDetailView.as_view(), name='permission-detail'),
    
    # Activity log endpoints
    path('activity-logs/', ActivityLogView.as_view(), name='activity-log-list'),
    path('activity-logs/<str:id>/', ActivityLogDetailView.as_view(), name='activity-log-detail'),
    
    # Authentication endpoints
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='auth-verify-otp'),
    path('auth/resend-otp/', ResendOTPView.as_view(), name='auth-resend-otp'),
    path('auth/refresh-token/', RefreshTokenView.as_view(), name='auth-refresh-token'),
    path('auth/verify-token/', VerifyTokenView.as_view(), name='auth-verify-token'),
] 
