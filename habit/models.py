from django.core.exceptions import ValidationError
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    # Добавим периодичность для дальнейшего отслеживания

    EVERY_DAY = 'Ежедневная'
    THREE_DAY = 'Трехдневная'
    FOR_WEEK = 'Еженедельная'

    FREQUENCY_CHOICES = (
        (EVERY_DAY, 'Ежедневная'),
        (THREE_DAY, 'Трехдневная'),
        (FOR_WEEK, 'Еженедельная'),

    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='создатель')
    place = models.CharField(max_length=25, verbose_name='место')
    timing = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=100, verbose_name='действие')
    is_pleasurable = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE,
                                      verbose_name='Связанная привычка', **NULLABLE)
    frequency = models.CharField(choices=FREQUENCY_CHOICES, default=EVERY_DAY, verbose_name='периодичность')
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', **NULLABLE)
    time_to_perform = models.CharField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'Я буду {self.action} в {self.timing} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
