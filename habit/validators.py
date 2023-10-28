import re
from rest_framework.serializers import ValidationError


class RelatedHabitValidator:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            related_habit = value.get(field)
            if related_habit:
                if related_habit and not related_habit.is_pleasurable:
                    raise ValidationError('Связанная привычка должна быть приятной')


# validator: У приятной привычки не может быть вознаграждения или связанной привычки.
class PleasantHabitValidator:
    def __call__(self, value):
        is_pleasurable = value.get('is_pleasurable')
        reward = value.get('reward')
        related_habit = value.get('related_habit')

        if is_pleasurable:
            if reward:
                raise ValidationError('Приятная привычка не может иметь вознаграждение.')
            if related_habit:
                raise ValidationError('Приятная привычка не может иметь связанную привычку.')
        return value


# validator: нельзя выполнять привычку реже 1 раза в неделю
class MinFrequencyValidator:
    def __call__(self, value):
        frequency = value.get('frequency')

        if frequency < 7:
            raise ValidationError('Привычку нельзя выполнять реже, чем 1 раз в 7 дней.')
        return value



