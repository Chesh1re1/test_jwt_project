import os
import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import Metric, MetricRecord

logger = logging.getLogger('celery')

@shared_task
def create_report():
    try:
        metrics = Metric.objects.count()
        metric_records = MetricRecord.objects.count()
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        report_content = f"""
            Дата: {timestamp}
            Всего метрик: {metrics}
            Всего записей метрик: {metric_records}
        """
        report_file = os.path.join(settings.REPORTS_DIR, 'fake_report.txt')
        absolute_path = os.path.abspath(report_file)
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(report_content)
        if os.path.exists(report_file):
            file_size = os.path.getsize(report_file)
            logger.info(f"✅ Файл создан успешно! Размер: {file_size} байт. Путь до файла: {absolute_path}")
        else:
            logger.error(f"❌ Файл не создан!")
        return f'Report created at {timestamp}'
    except Exception as e:
        raise e