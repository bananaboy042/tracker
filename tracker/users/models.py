from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Пользователь может иметь и username, и телефон
    """
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Номер телефона'
    )

    verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name='Код подтверждения'
    )

    code_sent_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Время отправки кода'
    )

    is_phone_verified = models.BooleanField(
        default=False,
        verbose_name='Телефон подтвержден'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.phone})"