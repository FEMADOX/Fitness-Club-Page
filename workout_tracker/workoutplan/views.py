from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from workoutplan.models import Exercise, Workout, WorkoutPlan
from workoutplan.serializers import (
    WorkoutPlanSerializer,
)

# class ExercisesView(generics.ListAPIView):
#     serializer_class = ExerciseSerializer
#     queryset = Exercise.objects.all()


# class WorkoutViewSet(viewsets.ModelViewSet):
#     serializer_class = WorkoutSerializer
#     queryset = Workout.objects.all()


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    queryset = WorkoutPlan.objects.all()

    def list(self, request: Request) -> Response:
        status_filter = request.query_params.get("status")
        queryset = self.queryset.all()

        if status_filter and status_filter.upper() in {"PENDING", "ACTIVE"}:
            queryset = queryset.filter(status=status_filter.upper())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        workouts_data = request.data.get("workouts")
        workout_plan_date = request.data.get("schedule_date")

        if workouts_data:
            workout_plan = WorkoutPlan.objects.create(
                schedule_date=workout_plan_date or timezone.now(),
                status="PENDING" if workout_plan_date else "ACTIVE",
            )

            workouts = [
                Workout(
                    exercise=Exercise.objects.get(pk=data.get("exercise")),
                    repetitions=data.get("repetitions"),
                    sets=data.get("sets"),
                    weight=data.get("weight"),
                )
                for data in workouts_data
            ]
            Workout.objects.bulk_create(workouts)
            workout_plan.workouts.add(*workouts)
            workout_plan.save()

            return Response(
                "Workout plan created successfully",
                status=status.HTTP_201_CREATED,
            )

        return Response(
            "Please provide a correct workout plan data",
            status=status.HTTP_400_BAD_REQUEST,
        )
