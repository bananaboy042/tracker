import threading
import time
from django.utils import timezone

from habbits.models import Habbit


class SchedulerThread(threading.Thread):
    def __init__(self, interval=10):
        super().__init__()
        self.interval = interval
        self.daemon = True
        self.running = True

    def run(self):
        while self.running:
            now = timezone.now()
            time_str = now.strftime('%H:%M')
            if time_str == '23:59':
                habits = Habbit.objects.all()
                for habit in habits:
                    if habit.next_execution_date == now.strftime('%Y-%m-%d') and habit.is_done_today == False:
                        habit.count = 0
                        habit.save()
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
            scheduler = SchedulerThread(interval=45)
            scheduler.start()
            print('🔄 Планировщик запущен через middleware!')

    def __call__(self, request):
        return self.get_response(request)