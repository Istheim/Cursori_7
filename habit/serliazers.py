from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from habit.models import Habit
from habit.validators import RelatedHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedHabitValidator(fields=['related_habit']),

            # validator времени выполнения
            serializers.MaxTimeValidator(field_name='time_to_perform', max_value="0:02:00")
        ]

    # validator проверки полей: связанной привычки и вознаграждения
    def rewardvalidate(self, value):
        related_habit = value.get('related_habit')
        reward = value.get('reward')

        if related_habit and reward:
            raise ValidationError('Нельзя одновременно указать связанную привычку и вознаграждение')
        return value
