from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Metric, Tag, MetricRecord
from .serializer import MetricSerializer, TagSerializer, MetricRecordSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get', 'post'], url_path='records')
    def get_cache_key(self, metric_id, user_id):
        return f'metric_records_{metric_id}_user_{user_id}'

    def handle_records(self, request, pk=None):
        metric = self.get_object()
        if request.method == 'GET':
            cache_key = self.get_cache_key(metric.id, request.user.id)
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)
            # Обработка GET запроса
            records = MetricRecord.objects.filter(metric=metric)
            serializer = MetricRecordSerializer(records, many=True)
            cache.set(cache_key, serializer.data, timeout=300)
            return Response(serializer.data)

        elif request.method == 'POST':
            # Обработка POST запроса
            serializer = MetricRecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(metric=metric)
                cache_key = self.get_cache_key(metric.id, request.user.id)
                cache.delete(cache_key)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path=r'records/(?P<record_pk>[^/.]+)')
    def get_current_record(self, request, pk=None, record_pk=None):
        metric = self.get_object()
        current_record = get_object_or_404(MetricRecord, metric=metric, pk=record_pk)
        serializer = MetricRecordSerializer(current_record)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class MetricRecordViewSet(viewsets.ModelViewSet):
    queryset = MetricRecord.objects.all()
    serializer_class = MetricRecordSerializer
    permission_classes = [IsAuthenticated]


