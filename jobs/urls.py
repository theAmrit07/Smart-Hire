from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, register, dashboard_stats, analyze_application

router = DefaultRouter()
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register, name='register'),
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('applications/<int:pk>/analyze/', analyze_application, name='analyze-application'),
]
