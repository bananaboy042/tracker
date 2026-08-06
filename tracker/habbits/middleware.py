import threading
import time
from datetime import datetime

class SchedulerThread(threading.Thread):
    def __init__(self, interval=10):
        super().__init__()
        self.interval = interval
        self.daemon = True
        self.running = True

    def run(self):
        while self.running:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f'Hello World! Время: {current_time}')
            time.sleep(self.interval)

# Глобальный экземпляр планировщика
scheduler = None

class SchedulerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._init_scheduler()

    def _init_scheduler(self):
        global scheduler
        if scheduler is None:
            scheduler = SchedulerThread(interval=10)
            scheduler.start()
            print('🔄 Планировщик запущен через middleware!')

    def __call__(self, request):
        return self.get_response(request)