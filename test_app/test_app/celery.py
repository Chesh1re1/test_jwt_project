import os
from celery import Celery
import logging

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_app.settings')

# Создаем экземпляр приложения Celery
app = Celery('test_app')

# Загружаем конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в tasks.py всех приложений
app.autodiscover_tasks()

logger = logging.getLogger('celery')
logger.setLevel(logging.INFO)  # Или DEBUG для более подробных логов
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)