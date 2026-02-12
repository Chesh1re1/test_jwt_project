from django.contrib import admin
from .models import Metric, Tag, MetricRecord
# Register your models here.

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(MetricRecord)
class MetricRecordAdmin(admin.ModelAdmin):
    list_display = ['metric_id', 'updated_at', 'created_at']
