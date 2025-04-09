from django.urls import path, include
from rest_framework_nested import routers
from user.views import UserViewSet
from blood.views import BloodRequestViewSet, DonorListView, Dashboard

# Main router
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('blood-requests', BloodRequestViewSet, basename='blood-requests')

# Nested routes
users_router = routers.NestedDefaultRouter(router, 'users', lookup='user')
users_router.register('blood-requests', BloodRequestViewSet, basename='user-blood-requests')

urlpatterns = [
    # Router endpoints
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    
    # Regular APIView endpoint
    path('donors-list/', DonorListView.as_view(), name='donor-list'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    
    # Authentication
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]