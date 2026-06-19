from django.db.models import Model, CharField, TextField, ForeignKey, PROTECT, DateField
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Color(Model):
    name = CharField(max_length=50, verbose_name="Название цвета")
    hex_code = CharField(max_length=7, unique=True, verbose_name="HEX код цвета")


class Habbit(Model):
    name = CharField(max_length=100, verbose_name="Название привычки")
    description = TextField(max_length=500, blank=True, verbose_name="Описание привычки")
    color = ForeignKey(Color, on_delete=PROTECT, verbose_name="Цвет привычки")
    start_date = DateField(default=now, verbose_name="Дата начала")
    end_date = DateField(null=True, blank=True, verbose_name="Дата окончания")

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

    def save(self, *args, **kwargs):
        """Переопределяем save для валидации"""
        # Валидация перед сохранением
        self.validate_dates()
        super().save(*args, **kwargs)



