from rest_framework import serializers

from workoutplan.models import Workout, WorkoutPlan

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:  # type: ignore[]
#         model = Category
#         fields = "__all__"


# class MuscleGroupSerializer(serializers.ModelSerializer):
#     class Meta:  # type: ignore[]
#         model = MuscleGroup
#         fields = "__all__"


# class ExerciseSerializer(serializers.ModelSerializer):
#     class Meta:  # type: ignore[]
#         model = Exercise
#         fields = "__all__"


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[]
        model = Workout
        fields = "__all__"


class WorkoutPlanSerializer(serializers.ModelSerializer):
    workouts = WorkoutSerializer(many=True)

    class Meta:  # type: ignore[]
        model = WorkoutPlan
        fields = ["workouts", "schedule_date", "status"]
