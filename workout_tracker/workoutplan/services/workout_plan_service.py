from typing import Any

from django.contrib.auth.models import AbstractBaseUser, User
from django.db.models import Count, QuerySet, Sum
from django.db.models.manager import BaseManager
from django.utils import timezone
from rest_framework import status

from workoutplan.models import Exercise, Workout, WorkoutPlan
from workoutplan.repositories.workout_plan_repository import WorkoutPlanRepository


class WorkoutPlanService:
    @staticmethod
    def get_all_workout_plans() -> QuerySet[WorkoutPlan]:
        return WorkoutPlanRepository.get_all()

    @staticmethod
    def get_all_workout_plans_of_user(
        user: User | AbstractBaseUser,
    ) -> BaseManager[WorkoutPlan]:
        return WorkoutPlanRepository.get_all(user)

    @staticmethod
    def get_workout_plan_of_user(
        user: User | AbstractBaseUser,
        workoutplan_pk: int,
    ) -> WorkoutPlan:
        return WorkoutPlanRepository.get_workoutplan(workoutplan_pk, user)

    @staticmethod
    def get_all_workout_plans_filtered(
        status_filter: str | None,
        user: User | AbstractBaseUser,
    ) -> BaseManager[WorkoutPlan]:
        if status_filter and status_filter.upper() in {"PENDING", "ACTIVE"}:
            return WorkoutPlanRepository.filter_by_status(status_filter.upper(), user)

        return WorkoutPlanRepository.get_all(user)

    @staticmethod
    def user_owner_workoutplan_validation(
        user: User | AbstractBaseUser,
        workoutplan_pk: int,
    ) -> dict[str, Any] | dict[str, bool]:
        if not WorkoutPlanRepository.workoutplan_exist(workoutplan_pk):
            return {
                "success": False,
                "message": "Workout Plan doesn't exist",
                "status": status.HTTP_404_NOT_FOUND,
            }
        if not WorkoutPlanRepository.is_user_owner(user, workoutplan_pk):
            return {
                "success": False,
                "message": "User is not owner of this Workout Plan",
                "status": status.HTTP_403_FORBIDDEN,
            }

        return {"success": True}

    # @staticmethod
    # def get_all_user_workout_plans(user_id: int) -> QuerySet[WorkoutPlan]:
    #     user = get_user_model().objects.get(pk=user_id)

    #     return WorkoutPlanRepository.get_by_user(user)

    @staticmethod
    def create_workout_plan(
        request: dict,
        user: User | AbstractBaseUser,
    ) -> dict[str, Any]:
        workouts_data = request["workouts"]
        workout_plan_date = request.get("schedule_date")
        workout_plan_user = user

        exercises_id = [workout_data["exercise"] for workout_data in workouts_data]
        exercises = Exercise.objects.in_bulk(exercises_id)

        workout_plan = WorkoutPlan.objects.create(
            user=workout_plan_user,
            schedule_date=workout_plan_date or timezone.now(),
            status="PENDING" if workout_plan_date else "ACTIVE",
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
    def generate_report(user: User) -> dict[str, Any]:
        workout_plans = WorkoutPlanRepository.get_all(user)
        total_workouts = workout_plans.aggregate(total=Count("workouts"))["total"]
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
            "total_workouts": total_workouts,
            "total_reps": total_reps,
            "total_sets": total_sets,
            "total_weight": total_weight,
        }
