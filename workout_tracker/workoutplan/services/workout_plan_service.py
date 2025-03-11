from django.contrib.auth.models import User
from django.db.models.manager import BaseManager
from django.utils import timezone

from workoutplan.models import Exercise, Workout, WorkoutPlan
from workoutplan.repositories.workout_plan_repository import WorkoutPlanRepository


class WorkoutPlanService:

    @staticmethod
    def get_all_workout_plans() -> BaseManager[WorkoutPlan]:
        return WorkoutPlanRepository.get_all()

    @staticmethod
    def get_filtered_workout_plans(
        status_filter: str | None,
    ) -> BaseManager[WorkoutPlan]:
        if status_filter and status_filter.upper() in {"PENDING", "ACTIVE"}:
            return WorkoutPlanRepository.filter_by_status(status_filter.upper())
        return WorkoutPlanRepository.get_all()

    @staticmethod
    def create_workout_plan(request: dict, user: User) -> dict:
        workouts_data = request.get("workouts")
        workout_plan_date = request.get("schedule_date")
        workout_plan_user = user

        if workouts_data:
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
                "success": True,
                "message": "Workout plan created successfully",
            }

        return {
            "success": False,
            "message": "Please provide a correct workout plan data",
        }
