from typing import Any

from django.contrib.auth.models import AbstractUser, User
from django.db.models import Count, F, Max, QuerySet, Sum
from django.db.models.manager import BaseManager

from common.exceptions import (
    NoWorkoutsWithExerciseException,
)
from workoutplan.models import Workout, WorkoutPlan
from workoutplan.repositories.workout_plan_repository import (
    ExerciseRepository,
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
        request: dict[str, Any],
        user: User | AbstractUser,
    ) -> WorkoutPlan:
        workout_plan_user = user
        workout_plan_date = request.get("schedule_date")
        workout_plan_status = request.get("status")

        workouts_data = request["workouts"]

        workouts = WorkoutPlanService.generate_workouts_from_request(workouts_data)

        return WorkoutPlanRepository.create(
            kwargs={
                "user": workout_plan_user,
                "workouts": workouts,
                "updated_date": workout_plan_date,
                "updated_status": workout_plan_status,
            },
        )

    @staticmethod
    def update(
        request: dict[str, Any],
        user: User | AbstractUser,
        pk: int,
    ) -> WorkoutPlan:
        WorkoutPlanRepository.workoutplan_exist(pk)
        workout_plan = WorkoutPlanRepository.get_workoutplan(pk, user)

        workout_plan_date = request.get("schedule_date")
        workout_plan_status = request.get("status")

        workouts_data = request["workouts"]

        workouts = WorkoutPlanService.generate_workouts_from_request(workouts_data)

        return WorkoutPlanRepository.update(
            workout_plan,
            kwargs={
                "workouts": workouts,
                "updated_date": workout_plan_date,
                "updated_status": workout_plan_status,
            },
        )

    @staticmethod
    def partial_update(
        request: dict[str, Any],
        user: User | AbstractUser,
        pk: int,
    ) -> WorkoutPlan:
        WorkoutPlanRepository.workoutplan_exist(pk)
        workout_plan = WorkoutPlanRepository.get_workoutplan(pk, user)

        request_list = {
            "workouts": request.get("workouts") or None,
            "schedule_date": request.get("schedule_date") or None,
            "status": request.get("status") or None,
        }
        fields_to_update = {key: value for key, value in request_list.items() if value}

        if fields_to_update.get("workouts"):
            fields_to_update["workouts"] = (
                WorkoutPlanService.generate_workouts_from_request(
                    fields_to_update["workouts"],
                )
            )

        return WorkoutPlanRepository.partial_update(
            workout_plan,
            fields_to_update["workouts"],
            fields_to_update["schedule_date"],
            fields_to_update["status"],
        )

    @staticmethod
    def generate_workouts_from_request(
        workouts_data: list[dict[str, int | float]],
    ) -> list[Workout]:
        exercises = ExerciseRepository.get_exercises_by_workouts(workouts_data)
        return [
            Workout(
                id=workout_data.get("id"),
                exercise=exercises[workout_data["exercise"]],
                repetitions=workout_data["repetitions"],
                sets=workout_data["sets"],
                weight=workout_data["weight"],
            )
            for workout_data in workouts_data
        ]

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
