from typing import Any

from django.contrib.auth.models import AbstractUser, User
from django.db.models import Count, F, Max, QuerySet, Sum
from django.db.models.manager import BaseManager
from django.utils import timezone
from rest_framework import status

from common.exceptions import (
    NoWorkoutsWithExerciseException,
)
from workoutplan.models import Exercise, Workout, WorkoutPlan
from workoutplan.repositories.workout_plan_repository import (
    WorkoutPlanRepository,
    WorkoutRepository,
)


class WorkoutPlanService:
    @staticmethod
    def get_all_workout_plans() -> QuerySet[WorkoutPlan]:
        return WorkoutPlanRepository.get_all()

    @staticmethod
    def get_all_workout_plans_of_user(
        user: User | AbstractUser,
    ) -> BaseManager[WorkoutPlan]:
        return WorkoutPlanRepository.get_all(user)

    @staticmethod
    def get_workout_plan_of_user(
        user: User | AbstractUser,
        workoutplan_pk: int,
    ) -> WorkoutPlan:
        return WorkoutPlanRepository.get_workoutplan(workoutplan_pk, user)

    @staticmethod
    def workout_plans_by_status(
        status_filter: str | None,
        user: User | AbstractUser,
    ) -> BaseManager[WorkoutPlan]:
        if status_filter and status_filter.upper() in {"PENDING", "ACTIVE", "ENDED"}:
            return WorkoutPlanRepository.filter_by_status(status_filter.upper(), user)

        return WorkoutPlanRepository.get_all(user)

    @staticmethod
    def create(
        request: dict,
        user: User | AbstractUser,
    ) -> dict[str, Any]:
        workouts_data = request["workouts"]
        workout_plan_date = request.get("schedule_date")
        workout_plan_status = request.get("status")
        workout_plan_user = user

        exercises_id = [workout_data["exercise"] for workout_data in workouts_data]
        exercises = Exercise.objects.in_bulk(exercises_id)

        workout_plan = WorkoutPlanRepository.create(
            user=workout_plan_user,
            schedule_date=workout_plan_date or timezone.now(),
            status=workout_plan_status or "ACTIVE",
        )

        workouts = [
            Workout(
                exercise=exercises[workout_data["exercise"]],
                repetitions=workout_data["repetitions"],
                sets=workout_data["sets"],
                weight=workout_data["weight"],
            )
            for workout_data in workouts_data
        ]
        Workout.objects.bulk_create(workouts)
        workout_plan.workouts.add(*workouts)
        workout_plan.save()

        return {
            "message": "Workout plan created successfully",
            "status": status.HTTP_201_CREATED,
        }

    @staticmethod
    def generate_plans_report(user: User | AbstractUser) -> dict[str, Any]:
        workout_plans = WorkoutPlanRepository.filter_by_status("ENDED", user)
        total_plans = workout_plans.count()
        total_exercises = workout_plans.aggregate(total=Count("workouts"))["total"]
        total_reps = Workout.objects.filter(workout_plans__in=workout_plans).aggregate(
            total=Sum("repetitions"),
        )["total"]
        total_sets = Workout.objects.filter(workout_plans__in=workout_plans).aggregate(
            total=Sum("sets"),
        )["total"]
        total_weight = Workout.objects.filter(
            workout_plans__in=workout_plans,
        ).aggregate(
            total=Sum("weight"),
        )["total"]
        return {
            "total_plans": total_plans,
            "total_exercises": total_exercises,
            "total_sets": total_sets,
            "total_reps": total_reps,
            "total_weight": total_weight,
        }

    @staticmethod
    def get_exercise_progress(
        user: User | AbstractUser,
        pk: int,
    ) -> dict[str, Any]:
        workouts = WorkoutRepository.get_workouts_ended(user)

        if not workouts.filter(exercise=pk).exists():
            raise NoWorkoutsWithExerciseException

        workouts = workouts.filter(exercise=pk)
        progress = workouts.aggregate(
            max_volume=Max(F("weight") * F("repetitions") * F("sets")),
            max_weight=Max("weight"),
            max_repetitions=Max("repetitions"),
            max_sets=Max("sets"),
        )

        return {
            "max_volume": progress["max_volume"] or 0,
            "max_weight": progress["max_weight"] or 0,
            "max_repetitions": progress["max_repetitions"] or 0,
            "max_sets": progress["max_sets"] or 0,
        }
