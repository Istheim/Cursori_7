from builtins import print
from datetime import datetime
import pytz
from celery import shared_task
from habit.models import Habit
from bot_post import handle


@shared_task
def every_day():
    timezone = pytz.timezone('Europe/Moscow')
    current_time_yek = datetime.now(timezone)
    current_time = current_time_yek.strftime('%H:%M')
    print(current_time)
    habits = Habit.objects.all()  # Получяем объекты Habit по фильтру раз в день

    for habit in habits:

        if habit.EVERY_DAY:  # каждые 24 часа
            if current_time == habit.time_habit.strftime('%H:%M'):  # проверяем чч:мм отправки
                handle(habit.get_habit)  # Выполняем отправку

        if habit.THREE_DAY:
            if (current_time_yek - habit.create_time).days > 3:  # каждые 72 часов раз в 3 дня
                if current_time == habit.time_habit.strftime('%H:%M'):  #
                    handle(habit.get_habit)

        if habit.FOR_WEEK:
            if (current_time_yek - habit.create_time).days > 7:  # каждые 172 часа раз в 7 дня
                if current_time == habit.time_habit.strftime('%H:%M'):  # проверяем чч:мм отправки
                    handle(habit.get_habit)
