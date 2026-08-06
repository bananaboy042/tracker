from django.db.models import Model, CharField, TextField, ForeignKey, PROTECT, DateField, JSONField, IntegerField
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from users.models import User
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import calendar


class Habbit(Model):
    name = CharField(max_length=100, verbose_name="Название привычки")
    description = TextField(max_length=500, blank=True, verbose_name="Описание привычки")
    color = CharField(max_length=7, verbose_name="Цвет привычки")
    start_date = DateField(default=now, verbose_name="Дата начала")
    end_date = DateField(null=True, blank=True, verbose_name="Дата окончания")
    last_executed = DateField(null=True, blank=True, verbose_name="Дата последнего выполнения")
    frequency = JSONField(
        verbose_name="Настройки периодичности",
        help_text="""
        Форматы:
        - Ежедневно: {"type": "daily", "interval": 1}
        - Через день: {"type": "daily", "interval": 2}
        - Еженедельно: {"type": "weekly", "days": [1, 3, 5]}  # 1-Пн...7-Вс
        - Ежемесячно: {"type": "monthly", "day": 15}  # 15-е число
        """
    )
    user = ForeignKey(User, on_delete=PROTECT, verbose_name="Пользователь")
    count = IntegerField(default=0, verbose_name='кол-во выполнений подряд')

    def __str__(self):
        return f'Привычка {self.name} создана {self.start_date}'

    @property
    def is_done_today(self):
        return self.last_executed == now().date()

    @property
    def is_today_execution(self):
        """Проверяет, является ли сегодня днем выполнения"""
        today = now().date()
        return self.next_execution_date != today

    @property
    def next_execution_date(self):
        today = now().date()
        freq_type = self.frequency.get('type')

        if freq_type == 'daily':
            interval = self.frequency.get('interval', 1)

            if self.start_date > today:
                return self.start_date

            days_since_start = (today - self.start_date).days
            if days_since_start % interval == 0:
                return today

            return today + timedelta(days=interval - (days_since_start % interval))

        elif freq_type == 'weekly':
            week_days = sorted(self.frequency.get('days', []))
            if not week_days:
                return today

            current_weekday = today.isoweekday()

            for day in week_days:
                if day > current_weekday:
                    return today + timedelta(days=day - current_weekday)

            return today + timedelta(days=(7 - current_weekday) + week_days[0])

        elif freq_type == 'monthly':
            target_day = self.frequency.get('day', 1)

            # Создаем дату для текущего месяца
            try:
                # Пытаемся создать дату с указанным днем
                next_date = today.replace(day=target_day)
            except ValueError:
                # Если день не существует (например, 31 февраля)
                # Берем последний день месяца
                last_day = calendar.monthrange(today.year, today.month)[1]
                next_date = today.replace(day=last_day)

            # Если дата уже прошла или сегодня
            if next_date <= today:
                # Переходим на следующий месяц
                next_date = today + relativedelta(months=1)
                try:
                    next_date = next_date.replace(day=target_day)
                except ValueError:
                    last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                    next_date = next_date.replace(day=last_day)

            # Проверяем, что дата не раньше start_date
            if next_date < self.start_date:
                # Если дата выполнения раньше start_date, корректируем
                diff_months = (self.start_date.year - next_date.year) * 12 + (self.start_date.month - next_date.month)
                if diff_months > 0:
                    next_date = self.start_date
                    # Ищем следующую дату после start_date
                    while next_date <= self.start_date:
                        next_date += relativedelta(months=1)
                        try:
                            next_date = next_date.replace(day=target_day)
                        except ValueError:
                            last_day = calendar.monthrange(next_date.year, next_date.month)[1]
                            next_date = next_date.replace(day=last_day)

            return next_date

        else:
            return max(today, self.start_date)

    def validate_dates(self):
        """Метод валидации дат"""
        today = now().date()

        if self.start_date < today:
            raise ValidationError({
                'start_date': f'Дата начала не может быть раньше сегодняшнего дня'
            })

        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': 'Дата окончания не может быть раньше даты начала'
                })
            if self.end_date < today:
                raise ValidationError({
                    'end_date': 'Дата окончания не может быть раньше сегодняшнего дня'
                })

    def validate_frequency(self):
        if not self.frequency:
            raise ValidationError({'frequency': 'Необходимо указать настройки переодичности.'})

        freq_type = self.frequency.get('type')

        if freq_type == 'daily':
            interval = self.frequency.get('interval')
            if not isinstance(interval, int) or interval < 1:
                raise ValidationError({
                    'frequency': 'Интервал должен быть положительным целым числом'
                })
        elif freq_type == 'weekly':
            days = self.frequency.get('days', [])
            if not isinstance(days, list) or not days:
                raise ValidationError({
                    'frequency': 'Для еженедельной периодичности укажите список дней недели'
                })
            if not all(isinstance(day, int) and 1 <= day <= 7 for day in days):
                raise ValidationError({
                    'frequency': 'Дни недели должны быть числами от 1 (Пн) до 7 (Вс)'
                })
        elif freq_type == 'monthly':
            day = self.frequency.get('day')
            if not isinstance(day, int) or not (1 <= day <= 31):
                raise ValidationError({
                    'frequency': 'День месяца должен быть числом от 1 до 31'
                })
        else:
            raise ValidationError({
                'frequency': f'Неизвестный тип периодичности: {freq_type}. Доступны: daily, weekly, monthly'
            })


    def save(self, *args, **kwargs):
        """Переопределяем save для валидации"""
        if self.pk is None:
            self.validate_dates()
        self.validate_frequency()
        super().save(*args, **kwargs)



