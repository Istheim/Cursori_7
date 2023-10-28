from rest_framework import serializers
from habit.models import Habit
from habit.validators import RelatedHabitValidator, PleasantHabitValidator, MinFrequencyValidator


# validator времени выполнения
def validate_time_to_perform(value):
    if value.total_seconds() > 120:
        raise serializers.ValidationError('Время выполнения не должно превышать 2 минуты.')


# validator проверки полей: связанной привычки и вознаграждения
def reward_validate(self, value):
    related_habit = value.get('related_habit')
    reward = value.get('reward')
    if related_habit and reward:
        raise serializers.ValidationError('Нельзя одновременно указать связанную привычку и вознаграждение')
    return value


class HabitSerializer(serializers.ModelSerializer):
    reward = serializers.CharField(validators=[reward_validate])
    time_to_perform = serializers.DurationField(validators=[validate_time_to_perform])

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedHabitValidator(fields=['related_habit']),
            PleasantHabitValidator(),
            MinFrequencyValidator()
        ]
