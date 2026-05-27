from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, DailyLogViewSet, ProgressAPIView, HeatMapCalendarAPIView

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'records', DailyLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('resumen/', ProgressAPIView.as_view(), name='progresssummary'),
    path('heat_map/', HeatMapCalendarAPIView.as_view(), name='heatmap'),
]