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



