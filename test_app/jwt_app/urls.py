from rest_framework.routers import DefaultRouter
from .views import MetricViewSet, TagViewSet, MetricRecordViewSet

router = DefaultRouter()

router.register(prefix=r'metrics', viewset=MetricViewSet, basename='metrics')
router.register(prefix=r'tag', viewset=TagViewSet, basename='tag')
'''
router.register(prefix=r'records', viewset=MetricRecordViewSet, basename='records')
'''

urlpatterns = router.urls