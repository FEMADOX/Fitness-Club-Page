import datetime
from typing import Any

from django.contrib.auth.models import AbstractUser, User
from django.db.models.manager import BaseManager
from django.utils import timezone

from common.exceptions import (
    ExerciseDoesntExistException,
    NoStatusPlansException,
    NoWorkoutsInPlanException,
    NoWorkoutsWithExerciseException,
    PlanDoesntExistException,
    UserDoesnExistException,
    UserIsntOwnerException,
)
from workoutplan.models import Exercise, Workout, WorkoutPlan


class WorkoutPlanRepository:
    @staticmethod
    def create(**kwargs: Any) -> WorkoutPlan:  # noqa: ANN401
        kwargs_dic: dict[str, Any] = next(iter(kwargs.values()))
        user, workouts, schedule_date, status = kwargs_dic.values()
        UserRepository.user_exist(user.pk)
        workout_plan = WorkoutPlan.objects.create(
            user=user,
            schedule_date=schedule_date or timezone.now(),
            status=status or "ACTIVE",
        )
        Workout.objects.bulk_create(workouts)

        workout_plan.workouts.add(*workouts) if isinstance(
            workouts,
            list,
        ) else workout_plan.workouts.add(workouts)

        return workout_plan

    @staticmethod
    def update(
        workout_plan: WorkoutPlan,
        workouts: list[Workout] | None = None,
        schedule_date: datetime.datetime | None = None,
        status: str | None = None,
    ) -> WorkoutPlan:
        if workouts:
            existing_workouts = WorkoutPlanRepository.update_workouts(workouts)

            if not existing_workouts:
                Workout.objects.bulk_create(workouts)

            workout_plan.workouts.clear()
            workout_plan.workouts.add(*workouts)
        workout_plan.schedule_date = schedule_date or timezone.now()
        workout_plan.status = status or "ACTIVE"
        workout_plan.save()

        return workout_plan

    @staticmethod
    def partial_update(
        workout_plan: WorkoutPlan,
        workouts: list[Workout] | None = None,
        schedule_date: datetime.datetime | None = None,
        status: str | None = None,
    ) -> WorkoutPlan:
        if workouts:
            # Separate new workouts from existing ones
            new_workouts = [
                Workout(
                    exercise=workout_data.exercise,
                    repetitions=workout_data.repetitions or 1,
                    sets=workout_data.sets or 1,
                    weight=workout_data.weight or 1,
                )
                for workout_data in workouts
                if not hasattr(workout_data, "id")
                and workout_data.exercise  # New workouts don't have an ID
            ]

            existing_workouts = WorkoutPlanRepository.update_workouts(workouts)

            # Bulk create new workouts
            Workout.objects.bulk_create(new_workouts) if new_workouts else None

            # Update the relationship
            workout_plan.workouts.clear()
            workout_plan.workouts.add(*new_workouts or existing_workouts)

        # Update other fields
        workout_plan.schedule_date = schedule_date or workout_plan.schedule_date
        workout_plan.status = status or workout_plan.status
        workout_plan.save()

        return workout_plan

    @staticmethod
    def update_workouts(
        updated_workouts: list[Workout],
    ) -> list[Workout]:
        """
        Updates the existing workouts with the data from updated workouts.

        Args:
            updated_workouts (list[Workout]): List of updated Workout objects.
        """

        existing_workouts = [
            Workout.objects.get(pk=workout_data.pk)
            for workout_data in updated_workouts
            if hasattr(workout_data, "id")  # Existing workouts have an ID
        ]

        if existing_workouts:
            # Update individual workout attributes
            for workout, workout_data in zip(
                existing_workouts,
                updated_workouts,
                strict=False,
            ):
                workout.exercise = workout_data.exercise or workout.exercise
                workout.repetitions = workout_data.repetitions or workout.repetitions
                workout.sets = workout_data.sets or workout.sets
                workout.weight = workout_data.weight or workout.weight

            # Bulk update workouts
            Workout.objects.bulk_update(
                existing_workouts,
                ["exercise", "repetitions", "sets", "weight"],
            ) if existing_workouts else None

        return existing_workouts

    # Searching
    @staticmethod
    def get_all(
        user: User | AbstractUser | None = None,
    ) -> BaseManager[WorkoutPlan]:
        if user:
            UserRepository.user_exist(user.pk)
            return WorkoutPlan.objects.filter(user=user)
        return WorkoutPlan.objects.all()

    @staticmethod
    def get_workoutplan(
        pk: int,
        user: User | AbstractUser,
    ) -> WorkoutPlan:
        WorkoutPlanRepository.workoutplan_exist(pk)
        WorkoutPlanRepository.is_user_owner(user, pk)
        return WorkoutPlan.objects.filter(user=user).get(pk=pk)

    @staticmethod
    def filter_by_status(
        status: str,
        user: User | AbstractUser,
    ) -> BaseManager[WorkoutPlan]:
        if not WorkoutPlan.objects.filter(user=user, status=status).exists():
            raise NoStatusPlansException

        return WorkoutPlanRepository.get_all(user).filter(status=status)

    # Validations
    @staticmethod
    def workoutplan_exist(workoutplan_pk: int) -> None:
        try:
            WorkoutPlan.objects.get(pk=workoutplan_pk)
        except WorkoutPlan.DoesNotExist as error:
            raise PlanDoesntExistException from error

    @staticmethod
    def is_user_owner(user: User | AbstractUser, workout_plan_pk: int) -> None:
        WorkoutPlanRepository.workoutplan_exist(workout_plan_pk)
        try:
            WorkoutPlan.objects.get(pk=workout_plan_pk, user=user)
        except WorkoutPlan.DoesNotExist as error:
            raise UserIsntOwnerException from error


class WorkoutRepository:
    @staticmethod
    def get_workouts_ended(
        user: User | AbstractUser,
    ) -> BaseManager[Workout]:
        workout_plans = WorkoutPlanRepository.filter_by_status(
            status="ENDED",
            user=user,
        )
        return WorkoutRepository.filter_by_plan(workout_plans)

    @staticmethod
    def filter_by_plan(workout_plan: BaseManager[WorkoutPlan]) -> BaseManager[Workout]:
        workouts = Workout.objects.filter(workout_plans__in=workout_plan)
        if not workouts.exists():
            raise NoWorkoutsInPlanException
        return workouts

    @staticmethod
    def filter_by_exercise(
        pk: int,
    ) -> BaseManager[Workout]:
        ExerciseRepository.exercise_exist(pk)
        if not Workout.objects.filter(exercise=pk).exists():
            raise NoWorkoutsWithExerciseException
        return Workout.objects.filter(exercise=pk)

    @staticmethod
    def workouts_by_exercise(
        pk: int,
        workouts: BaseManager[Workout],
    ) -> BaseManager[Workout]:
        ExerciseRepository.exercise_exist(pk)
        if not workouts.filter(exercise=pk).exists():
            raise NoWorkoutsWithExerciseException
        return workouts.filter(exercise=pk)


class ExerciseRepository:
    @staticmethod
    def get_exercises_by_workouts(workouts: list) -> dict[Any, Exercise]:
        exercises_pk = [workout_data["exercise"] for workout_data in workouts]

        ExerciseRepository.exercises_exist(exercises_pk)

        return Exercise.objects.in_bulk(exercises_pk)

    @staticmethod
    def exercise_exist(pk: int) -> None:
        try:
            Exercise.objects.get(pk=pk)
        except Exercise.DoesNotExist as error:
            raise ExerciseDoesntExistException from error

    @staticmethod
    def exercises_exist(exercises_pk: list[int]) -> None:
        exercises = Exercise.objects.filter(pk__in=exercises_pk)
        missing_exercises = set(exercises_pk) - set(
            exercises.values_list("pk", flat=True),
        )
        if missing_exercises:
            raise ExerciseDoesntExistException


class UserRepository:
    @staticmethod
    def user_exist(pk: int) -> None:
        try:
            User.objects.get(pk=pk)
        except User.DoesNotExist as error:
            raise UserDoesnExistException from error
