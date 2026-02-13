from django.db import models

class Metric(models.Model):
    name = models.CharField(
        verbose_name='Название'
    )

    class Meta:
        db_table = 'metric'
        verbose_name = 'Метрика'
        verbose_name_plural = 'Метрики'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название'
    )

    class Meta:
        db_table = 'tag'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class MetricRecord(models.Model):
    metric = models.ForeignKey(
        Metric,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Метрика'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тэг'
    )
    data = models.CharField(
        verbose_name='Данные'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        db_table = 'metricrecord'
        verbose_name = 'Запись метрики'
        verbose_name_plural = 'Записи метрики'
