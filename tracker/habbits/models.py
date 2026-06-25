from django.db.models import Model, CharField, TextField, ForeignKey, PROTECT, DateField, JSONField
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Color(Model):
    name = CharField(max_length=50, verbose_name="Название цвета")
    hex_code = CharField(max_length=7, unique=True, verbose_name="HEX код цвета")

    def color_preview(self):
        return mark_safe(
            f'<div style="background-color: {self.hex_code}; width: 30px; height: 30px; border: 1px solid #ddd;"></div>'
        )

    color_preview.short_description = 'Цвет'


class Habbit(Model):
    name = CharField(max_length=100, verbose_name="Название привычки")
    description = TextField(max_length=500, blank=True, verbose_name="Описание привычки")
    color = ForeignKey(Color, on_delete=PROTECT, verbose_name="Цвет привычки")
    start_date = DateField(default=now, verbose_name="Дата начала")
    end_date = DateField(null=True, blank=True, verbose_name="Дата окончания")
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
        # Валидация перед сохранением
        self.validate_dates()
        self.validate_frequency()
        super().save(*args, **kwargs)



